---
title: "Python dataclasses, a package full of surprises"
description: "When it comes to serialisation, premature optimisation is worth the effort. A cautionary tale of Python's dataclass library."
author: "Lennard Berger"
date: "2023-05-14"
categories: [python,dataclasses]
---

> Premature optimisation is the root of all evil

Virtually every software engineering lecture nowadays contains this wisdom by Sir Tony Hoarse.
If you ask me, this truth has been perpetuated for good reason. With modern computing power, there are few motivations to worry about low-level code optimisation.
Certainly, as it comes towards the triangle of software development, resources are inexpensive compared to engineering time, and more simple and maintainable software design is preferable over performance.
But to every rule, there are exceptions. Today we will discuss one of the stumbling blocks in our software landscape: **serialisation**.

Nearly any software must deal with this seemingly simplistic problem. Your program defines an input and an output, and you would like to be able to make deterministic assessments on the program’s behaviour based on this. Preferably before runtime (think of tests).
Depending on your programming paradigm, this may not be easy, or even achievable.

## Programming paradigms

At [YUKKA Lab][yukka] we work with high iteration speed (we typically ship a new release for testing at least once a week) across teams. This is why we love Python. A researcher can create an analysis or improve our existing pipelines. As we make progress across teams, we want to start shipping features for our customers.

With Python, this is as easy as loading a JSON document with the built-in JSON module and serving it via an API endpoint.
For some products we rely on dynamic data stores (NoSQL) which allows us to adjust schema on-the-fly, thus significantly accelerating iteration speed from the lab to customers.

This, however, comes at a price. Ensuring stability and backwards-compatibility is more time-consuming. (Software) contracts need to be written between individual components to ensure the lights keep on.

## Enter dataclasses

Originally introduced in Python 3.7 they bring a simple, yet missing feature to Python. Conceptually, `dataclasses` are the equivalent of C structs or data containers in other languages.
Dataclasses are convenient, as they:

- Offer type hints and bundle state.
- Can be extended via properties to be hashable, immutable etc. (this is difficult to achieve with dictionaries)
- Offer advanced features such as default initialisers and (de)serialisation.

That’s great, thanks Python 3.7, we’ll use that! With the advent of static type checkers in Python 3.5 this helps to greatly cut down the number of errors relating to IO tasks before runtime.

Now that we have defined our data structure(s), it’s time to serialise and deserialise some data. We can do that using:

- ?
- `asdict` from the dataclasses library, which exports a dictionary

Huh. This is interesting, we can serialise data, but we cannot reverse this operation with the standard library. After a quick Googling, we find ourselves using `parse_obj_as` from the pydantic library. Done for the day, or are we?

## Dataclasses are slow

Remember that dataclasses are conceptually like structs, but not really. If you follow this recipe, you may be headed for a few really bad surprises:

- Your constructor takes 5x longer than you are used to. [see [1]](#ref1)
- Accessing your data classes takes 20% longer than you are used to [see [1]](#ref1)
- `asdict` is incredibly slow, in fact for large objects it may be unsuitable [see [2]](#ref2)
- Unsurprisingly, `parse_obj_as` is also really slow.

Huh? You suddenly introduced a huge bottleneck into your software that may make it un-runnable? Let’s dive into these issues one at a time.

## Dataclasses are classes, not dictionaries

Dataclasses are classes, not dictionaries. They do not use hash tables for member access. Surprisingly, the runtime implication for accessing attributes is **not** O(1), it is 20% slower than using dictionaries [see [1]](#ref1). This time can quickly add up.

Another interesting fact is that class instantiation is significantly slower than dictionary creation [see [4]](#ref4). This can be helped by using slots (as per the [documentation](https://docs.python.org/2/reference/datamodel.html#slots)).

However, to the best of our own estimation, even with slots=True, class instantiation is approximately 3x slower than creating dictionaries.

## Dataclasses perform runtime checks

This should have been obvious from the documentation, but the implications of this statement are certainly not. When a dataclass is created, all attributes are fetched via type. When you serialise or deserialise data those attributes are verified via type [see [2]](#ref2). `type` (and by extension `isinstance`) should be avoided at all costs, because they are excruciatingly slow, and Python hasn’t really been designed to work in such a way [see [3]](#ref3).

There is a partial workaround to this behaviour which is to disable some of the initialisation code using `init=False`. However, this is explicitly discouraged in the documentation, because this can have impacts on data consistency.

## Dataclasses design choices

With the above observations in place, we can notice that dataclasses have several distinct disadvantages that may make them unsuitable for production use. They have not been designed around static type checkers. However, this lack of before-runtime data checks can be seen as a severe design limitation of the library. Consider the following:

```python
def as_dict(klass: T) -> Union[dict, list[dict]]:
    if is_dataclass(klass):
        return {
            key: as_dict(value)
            if is_dataclass(value) or isinstance(value, list)
            else value
            for key, value in klass.__dict__.items()
        }
    elif isinstance(klass, list):
        return [as_dict(k) for k in klass]
    else:
        raise TypeError(f"{klass.__name__} is not a dataclass")

```
This code does not have type guards concerning types where:

- Classes are unknown dataclasses
- Data is not contained within the standard data types
- Union types in lists

But it performs in 1/3 of the time of asdict, and it does its job reasonably well. This is because in many cases, we can assume data types to be correct before runtime and wrapping an exception block around json.loads may be sufficient as a safeguard.

In contrast, the dataclasses library (and companions) are built with the assumption that everything is always unsafe, and thus very costly checks are performed.

One can argue that this is a deliberate design decision, and I may be inclined to agree. But the broader implications are not really discussed in the documentation.

## Where to go from here

Dataclasses are a very useful tool for what they are designed for, and I would hope that future iterations of the library will bring improved support for static type checks and optional runtime checks.
Before we start ruling them out entirely however, I wanted to give some optimisations to consider:

- If you are not using recursive data structures, init=False may be for you
- If you are not mutating state and use Python 3.10 or newer, `slots=True` is for you (this will speed up access)

If you deem dataclasses’ performance issues intolerable, a notable alternative may be TypedDict’s from the typing module. It has been introduced in Python 3.9 as purely syntactic sugar over built-in dictionaries. Several additions have been introduced which make this alternative very promising, notably:

- [NotRequired](https://docs.python.org/3/library/typing.html#typing.NotRequired), the equivalent of optional arguments to dictionaries in Python 3.11
- [MappingProxyType](https://docs.python.org/3/library/types.html#types.MappingProxyType) can be used for immutable and [hashable](https://github.com/python/cpython/issues/87995) collections (Python 3.12 and later)

Thus, we could port a dataclass in Python 3.12 like so:

```python
from dataclasses import dataclass
from typing import Optional, NotRequired, TypedDict, cast
from types import MappingProxyType



@dataclass(frozen=True)
class InventoryItem:
  unit_price: float
  name: Optional[str] = None
  quantity_on_hand: int = 0



class InventoryItemDict(TypedDict):
  unit_price: float
  quantity_on_hand: int
  name: NotRequired[str]


item = InventoryItem(
  name="technical debt", 
  unit_price=10
)

item_dict = MappingProxyType(InventoryItemDict(
  name="technical debt",
  quantity_on_hand=1,
  unit_price=10
))


# This is Python 3.12 code
assert hash(item) == hash(item_dict)
assert cast(InventoryItem, item_dict) == item
```

With the distinct disadvantage that we do not have default initialisers. However, our code can remain (almost) identical at (almost) identical performance, with the benefit of having immutable, hashable and typed data containers.

The biggest showstopper for widespread adoption should be the fact that this consists of multiple preview features. Python 3.12 is expected to be widely available no earlier than August 2023. It remains to be seen whether this can serve as a good alternative in the future.

### References

<a id="ref1"></a>[1] Arne, "Python 3 - Which one is faster for accessing data: dataclasses or dictionaries?" — [stackoverflow.com](https://stackoverflow.com/questions/55248416/python-3-which-one-is-faster-for-accessing-data-dataclasses-or-dictionaries/55256047#55256047) [Accessed 29-07-2023]

<a id="ref2"></a>[2] ostrokach, "Why is `dataclasses.asdict(obj)` > 10x slower than `obj.__dict__()`" — [stackoverflow.com](https://stackoverflow.com/q/52229521) [Accessed 29-07-2023]

<a id="ref3"></a>[3] Mitchell Snaith, "Why is checking isinstance(something, Mapping) so slow?" — [stackoverflow.com](https://stackoverflow.com/questions/42378726/why-is-checking-isinstancesomething-mapping-so-slow/42379814#42379814) [Accessed 29-07-2023]

<a id="ref4"></a>[4] Andrew Dalke, "Class instantiation performance" — [dalkescientific.com](http://www.dalkescientific.com/writings/diary/archive/2006/03/19/class_instantiation_performance.html) [Accessed 29-07-2023]

[yukka]: https://www.yukkalab.com

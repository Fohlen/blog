---
title: "Why do machines learn at all?"
description: "A soft introduction into Statistical Learning Theory and why Machine Learning works"
author: "Lennard Berger"
date: "2026-09-06"
categories: [python,machine learning,statistics]
---

I believe for a long time people were pretty skeptical on whether machines learn at all.
Even though LLMs have driven home the point on **if** machines can learn, the **why** is still pretty opaque.
There's this famous XKCD comic which describes this pretty accurately.

![Machine learning comic on XKCD](https://imgs.xkcd.com/comics/machine_learning.png)

In my humble opinion there is a large plethora of material out there which describes **how** to make machines count your beans. A simple Amazon Book search returns some 2000 thousand or more books for _Introduction to Machine Learning_.
The recipe is usually simple:

1. visualize a data set
2. notice it is $X$-distributed
3. get some intuition on how regression works, then fit it to $X$-distributed
4. repeat the same with more complex data
5. work through a bunch of algorithms and finally Deep Learning, fit very complex data

Even the definite book on Deep Learning [see [1]](#ref1) does not have an explicit chapter on **WHY** machines learn.

I will try to shed some light on Statistical Learning Theory [see [2]](#ref2), which underpins modern machine learning, even when Vapnik and his colleagues usually are not in the spotlight. The abstract of the book reads as follows:

>  The statistical theory of learning and generalization concerns the problem of choosing desired functions on the basis of empirical data.

Hmm, ok, reads pretty opaque: _"choosing desired functions on the basis of empirical data"_, what the hell does that even mean?

## It all starts with a distribution

Suppose you want to predict population weight based on some factor, say, height.
You will go out and sample two distributions: $H$ and $W$.

These distributions are normal: the average might be 165 centimers or such, depending on which population you sample. Some people will be small, some will be taller. Likewise, there'll be an average weight, some will be slimmer, some will be heavier.

Physics alone dictates some relationship between the two: if you are taller, you are likely heavier.

Suppose you want to fit a function $f(h) = w$ calculating the weight of an individual from its height.
To do so, you will have a few choices.

#### Using the full distribution

You can use the sample data of the distribution $W$ and $H$ work out the optimal function according to whichever criteria you desire.

#### Using the distribution parameters

Instead of using the sample data, you can use the distribution parameters: mean and standard deviation. This narrows down the data you have to retain to four parameters. You loose some precision. You will still have to carry out substantial calculations (create a normal distribution from the parameters and fit a function).

#### Work out a regression model

This boils down to: $y = mx + b$. Hey! You narrowed down the number of parameters to three, and you **eliminated** any further computation.
On the negative side, you suddenly introduced a lot of noise, essentially you did the following:

$F(W|H) + N$, where you introduced some amount of uncertainty, or **noise** to the original distribution.

This can be expressed as:

$f(w) = x + n$

## Improving your estimate

If you want a more precise estimate, you can calculate delta (difference) between the estimated value and the actual value. This is what mean standard error does, precisely:

$$MSE = \frac{1}{n} \sum{n}(y_i-y_{\hat{i}})^2$$

From an information theoretic perspective, MSE is the [**optimal** classifier for a linear regression problem](https://plato.stanford.edu/entries/bounded-rationality/bias-variance-decomp.html).



## How much information do you need?

In my academic career we were never bothered to read Shannon's original paper on information theory [see [3]](#ref3).
I wish I had done this sooner, because it would have made me realise that there is a hard limit on the amount of compression (how many parameters you can save) one can do.

Shannon understood pretty early on that one can quantify the amount of noise in a signal (distribution), which became known as the measure of information entropy (the average level of uncertainty in a distribution).

The more general case was later developed by Kolgomorov into what is known as Kolgomorov complexity [see [4]](#ref4) and gives hard limits on how much compression can happen in dependant and non-normal distributions.

## Where does our bias come into play?

When we want to fit a regression model we **assumed** that our sample is normally distributed, and thus we have introduced a **bias**. Bias is essentially the deviation between our assumption, and the true data genereting process.
We have no access to the data generating process (we do not know or control or produce the genes and environment which make people tall or thin), and thus we **must** sample.

Ideally we want to minimise this bias. If we could we would want it to be $0$, so that our estimate is very precise.
This is what Solomonoff calls the theory of inductive inference [see [5]](#ref5):

> the best possible scientific model is the shortest algorithm that generates the empirical data under consideration

It has later on become known as the minimum description length principle and it was largely popularised by the _"no free lunch theorems"_ [see [6]](#ref6). 

The no free lunch theorems postulise that there is no single best model, indeed the best model comes directly from the data.

Opponents of the no free lunch theorems have proclaimed that they are nice theoretical constructs, but they provide no value when you actually want to fit models.

Thats why  I will propose a more modern approach towards machine learning: Statistical Learning Theory (SLT).

## Statistical Learning Theory

At the heart of Statistical Learning Theory [see [7]](#ref7) is the characterisation of _function estimators_. A general model of learning (according to SLT) requires:

1. > A generator (G) of random vectors $x \in \mathbb{R}^2$ drawn independently from a fixed but unknown probability distribution function F(x)
2. > A supervisor (S) who returns an output value $y$ to every input vector $x$, according to a conditional distribution function $F(x|y)$, also fixed but unknown
3. > A learning machine (LM) capable of implementing a set of functions $f(x, \alpha), \alpha \in \Lambda$, where $\Lambda$ is a set of parameters

A linear regression is exactly this: we draw from a conditional distribution $F(H|W)$ and we create a function with sufficient parameters to represent their relationship. In SLT you have the best possible model when you minimise the deviation between $G$ and $S$, in other words when $G - S = 0$.

In terms of SLT this is called the **loss** function $L(y, F(x, \alpha))$ (for the machine learning readers this will be **VERY** familiar). Estimating the loss of a function is called **risk**, and reducing the bias of a loss is the process of optimisation itself.

At this point we have turned $180°$ and jumped straight into the foundations of modern (deep) machine learning - all from relatively simple concepts.

I will want to recap the following lesson to you: both machine learning and inductive inference converge on the fact that the least biased model is the **best** possible model.

## Okay, and?

One consequence of inductive inference that has been overlooked by much of the literature is that we should phrase inductive bias as a **necessary condition** for learning. Given a generator $G$ and a supervisor $S$, learning occurs **ONLY** if a set of parameters $\Lambda$ exist such that $F(x, \alpha)$ approximates $S$.

I will illustrate why this idea was extremely radical and dismissed during its hayday.

If $G - S = 0$ is a tautology. If we could have perfect models, we would know $G$, the true data generating process. We can't. The butterfly effect applies.

We also have another insight here. As $G - S \rightarrow 0$ the model becomes trivial. The less bias, the more certain our prediction, the easier it becomes to predict. Vapnik called this the Empirical Risk Minimisation (ERM) inductive principle.

If $S$ is a conditional distribution of $G$, and an approximation exists (a function with enough paratemers), $F(x, \alpha)$ **will be attracted by the optimum**.

As our bias becomes zero, in a dataset that has a conditional relationship, the function **MUST** approximate this relationship. If this wasn't the case, for instance the loss was not a valley but rather flat, no learning would occur, and optimisation would converge immediately.

There is a lesson hidden among the no free lunch theorems. It is not that choosing a specific model is wrong per-se, but rather, all models are forced upon the same trajectory eventually.

## What conclusions should we take from this?

In order to make machines learn we need _"only"_ choose $S$ in a way that it closely resembles $G$.
Hey! This is our inductive bias. Others might call it _"experience"_ or "_gut feeling"_.

When people tell young Computer Science or Data Science students to think carefully about feature engineering, this isn't light-headed advice. **The data is the algorithm**. Choose your $S$ wisely, and you will get a learning machine, it is guaranteed and **must obey**.

How exactly induction works, and more precisely, how we can leverage induction to our advantage is an active field of study. [Oran Looney wrote a great blog post regarding this topic](https://www.oranlooney.com/post/rose-petals/).
I would be greatly interested in any new research on evolutionary algorithms (or else) concerning the study of induction, send me a message if you want to share your exciting research or thoughts!

### References

<a href="ref1"></a>[1] Goodfellow, I., Bengio, Y. and Courville, A. (2016) Deep Learning. MIT Press, Cambridge.
http://www.deeplearningbook.org

<a id="ref2"></a>[2] Vapnik, V. N. (1999). An overview of statistical learning theory. IEEE transactions on neural networks, 10(5), 988-999.

<a id="ref3"></a>[3] Shannon, C. E. (1948). A mathematical theory of communication. The Bell system technical journal, 27(3), 379-423.

<a id="ref4"></a>[4] Kolmogorov, A. N. (1998). On tables of random numbers. Theoretical Computer Science, 207(2), 387-395.

<a id="ref5"></a>[5] Solomonoff, R. J. (1964). A formal theory of inductive inference. Part I. Information and control, 7(1), 1-22.

<a id="ref6"></a>[6] Wolpert, D. H., & Macready, W. G. (1997). No free lunch theorems for optimization. IEEE transactions on evolutionary computation, 1(1), 67-82.

<a id="ref7"></a>[7] Vapnik, V. N. (1999). An overview of statistical learning theory. IEEE transactions on neural networks, 10(5), 988-999.

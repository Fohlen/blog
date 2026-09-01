---
title: "How much calories does an LLM burn?"
description: "A whimsical attempt at making sense of LLM energy consumption"
author: "Lennard Berger"
date: "2024-09-20"
categories: [llm,deep learning,ai,energy]
---

> Every request to GPT-4 burns 430 calories, approximately 17% of an average male diet

A clickbait quote from me for the dear reader, to tease you into the topic of AI energy consumption, something many people rarely give any thought to.

You might wonder, how did I come up with this number? Glad you ask, I'd like to do the math with you.

## Let's fuel an LLM

Many people are aware of the fact that large language models consume lots of energy. It is in the name, "large" models. 
We don't have the exact tally for GPT-4, as the technical paper does not outline it. 
[see [1]](#ref1) went down the rabbit hole to find out how much energy GPT-3 and Meta's LLama family of models consumed during training.

In this blog post, we will use the numbers for LLama-combined, which performs head-to-head with GPT4 (depending on the benchmark).
For training the combined LLama model, **2638000** kWh were necessary.

Your response to that number will likely be: ok, but I don't care, this number means nothing to me.

No worries there, I reacted exactly the same way, humans aren't wired to make sense of millions of kilowatt-hours.

We'll break down how much energy that actually is:

1. one killowat hour multiplies out to an energy value of 860421 calories
2. according to the Energy Information administration, an average household consumes 899 kwH per month [see [2]](#ref2)
3. an average female should eat about 1600 to 2000 calories, whereas an average male should consume 2000 to 2500 calories
4. an average american household has 3.13 members [see [3]](#ref3)

From this we can work out the math:

Per citizen, we need 287 kilowatt hours per month, and an additional 0.08 kwH for food (75000 calories), which is 3445.2 kWh per year.

When training mixed LLama we consumed the energy budget of 765 citizens for an entire year.

Equivalently, we could nourish 25 doctorate students, until they are 30 years old, which is the average age for a doctorate [see [4]](#ref4).

Great, armed with the knowledge of 25 doctorate students, we go to work!

## The energy consumption of inference

The true energy consumption of inference isn't exactly known, but the best guestimates provide a number of 0.0005 kWh per request.

This is ~430 calories, roughly one plate of prawn spaghetti (if one can believe the BBC).

Using one of our 25 doctorate students, we could work out how much time they would have to answer the same request.
We would assume they have access to a library (no digital devices), and are told the question verbatim.

Energy consumption throughout the day is relatively uniform (except for sport), so 104 calories per hour.

The math works out to:

```
(((430 calories) / (104 calories / hour)) / 25 people) * 1/60 hour ~ 10 minutes / people
```

So for every request to GPT-4, we could put our 25 doctorate students to work for 10 minutes to devise an answer.
Having 25 doctorate students agree on a response is unlikely, but the equation is pretty mind-boggling.

OpenAI has claimed GPT-5 will reach [PhD-level intelligence](https://www.linkedin.com/pulse/openai-cto-predicts-chatgpt-achieve-phd-level-within-two-anton-dubov-auicc/). 
Thus, every request could be equated with 25 PhD students working 10 minutes for you. Now that is a number one can **let sink in**.

## On a more serious note

The consumption presented here is a guestimate based on available data and comes backed in with two assumptions:

1. our PhD students don't travel etc - also, they're American (other countries have much lower energy estimates)
2. GPT-4 and GPT-5 will be more energy intensive (but with advances in chips they may not need to be)

However, I think it gives a much better feeling of what exactly is our quality standard for an LLM.

If I put 25 PhD students to work, I expect them **not** to hallucinate, simply.
On the other hand, if we believe the marketing around LLM, if we put the same amount of energy into an LLM, its not as tragic.

That's why it is important to spell out energy consumption in a currency we understood (such as human labour hours), rather than an abstract quantity (such as kWh).

### References

<a id="ref1"></a>[1] Sunder Ali Khowaja, Parus Khuwaja, Kapal Dev, Weizheng Wang and Lewis Nkenyereye, "ChatGPT Needs SPADE (Sustainability, Privacy, Digital Divide, and Ethics) Evaluation: A Review" — *Cognitive Computation*, pp. 1--23, Springer, 2024.

<a id="ref2"></a>[2] "Frequently Asked Questions (FAQs) - U.S. Energy Information Administration (EIA)" — eia.gov. https://www.eia.gov/tools/faqs/faq.php?id=97&t=3 (accessed 19-09-2024).

<a id="ref3"></a>[3] "Average Family Size in the U.S. 1960-2022" — Statista. https://www.statista.com/statistics/183657/average-size-of-a-family-in-the-us/ (accessed 19-09-2024).

<a id="ref4"></a>[4] "Age Distribution of Doctorate Recipients U.S. 2021" — Statista. https://www.statista.com/statistics/240152/age-distribution-of-us-doctorate-recipients/ (accessed 19-09-2024).

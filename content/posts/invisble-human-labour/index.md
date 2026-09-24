---
title: "Human labour is largely invisible to AI"
description: "This blog post tries to reconcile the current AI research landscape with the real world"
author: "Lennard Berger"
date: "2026-09-24"
categories: [machine learning, artifical intelligence]
---

I am beginning this blog post with a quote of Ilya Sutskever [from a podcast with Dwarkesh Patel](https://www.dwarkesh.com/p/ilya-sutskever-2):

> Yeah. This is one of the very confusing things about the models right now. How to reconcile the fact that they are doing so well on evals? You look at the evals and you go, “Those are pretty hard evals.” They are doing so well. But the economic impact seems to be dramatically behind. It’s very difficult to make sense of, how can the model, on the one hand, do these amazing things, and then on the other hand, repeat itself twice in some situation?

In my opinion this echoes a plethora of researchers in the AI field. Recently [Jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev) has been all anyone can talk about, and it asks the same exact question:

> Models have been superhuman at chat for years, so where is all the automation? This has been my driving question for the last four years.

How is it that these extremely smart people seem to independantly arrive at the same, apparently implausible conclusion?
I will try and investigate this in three chapters:

1. Generative AI needs well-defined problems
2. Vast amounts of human labour does not quality as well-defined
3. No one is infallible to groupthink.

## Generative AI needs well-defined problems

It is no secret by now that LLMs are very good at _"narrow-intelligence”_. Given one example of a family of tasks they do remarkably well at transferring the learned skill to other tasks of the same category. Jay Kruer [wrote an excellent blog post](https://dank.systems/posts/2026-09-15-ai-bear.html) in which he summaries the current AI landscape as:

> the models generalize well only on tasks within a small neighborhood of the specific tasks they've been trained on, and even then with severe caveats. the frontier labs have developed a general recipe to teach models almost any specific task enjoying clearly defined levels of task performance; many tasks are covered in the training data; but even small perturbations within a covered class of task result in outright failure or reward hacking.

Tellingly this is why harness engineering has become so big in the last few months. 

Given a stable reward signal, such as a lean theorem prover, and many concurrent agents, you can essentially brute-force the Pareto frontier for a wide variety of well-defined problems. 

Although this idea has been postulated a long time ago (you can read [my post on Statistical Learning Theory for a summary](/posts/why-machines-learn-at-all/)) it is not a minor achievement, and it’s cool to witness this in real life on incredibly challenging problems. 

In my present blog post I will dig deeper into one consequence of current generative AI models. As Jay puts it:

> the present problem of reward hacking can be solved only by rigorous specification by domain experts

Lean is **exactly** such a system. Rigorous specification by domain experts curated over 13 years. If OpenAI had to pay for the implementation of a theorem prover, including MathLib, the game would look substantially different. Essentially they have free-loaded this expertise.

Likewise, OpenAI and Microsoft free-loaded writing code (**not** software engineering) from the open source community. Some FOSS projects lend themselves perfectly for this sort of training. Very well specified documentation corresponding to a single function. StackOverflow accepted answers shares the same characteristics. Experts that painstakingly accrued knowledge and put it into a well-defined specification, given a problem description.

These characteristics extend to a number of other fields, notably RCVEs, medicine (where specification is crucial), chip design, aerospace and a few more.
All of these are industries where experts were paid a **lot** of money, over extended periods of time, to collect and specify problems and their solutions.

## Vast amounts of human labour does not qualify as well-defined

I think this point has been discussed ad-absurdum for Software Engineering. Software Engineering encompasses writing code, but it is not the only activity a Software Engineer performs. Here’s a tentative and definitely incomplete lists of other activities we think of when we say someone is working as a Software Engineer:

- talking to a customer and other stakeholders
- defining the problem a customer has based on conversations with them
- aligning with product managers
- testing assumptions, translating them into specifications
- testing code
- deploying software
- quality assurance and handoffs together with the product team
- adding metrics and tracking them (both for observability and success)
- observing, analysing and creating procedures to improve all of the above

Now, tick off: how many of those have a rigorously defined schema?

Let’s say, for fun, we’re called **EverythingAI** and we wanted to train a model to do all of the above.
Firstly, we need a lot of domain experts in each of these steps, and we need to record them. This is [allegedly what Meta has been doing](https://blog.pragmaticengineer.com/the-pulse-meta-wanted-to-reduce-teams-by-60-because-of-ai/).

We will very quickly run into a trade-off: we will need to hire and train senior personnel to specify even the most menial of tasks, such as would traditionally be performed by junior QA or software engineers.

Like in any other business, [the law of diminishing returns](https://www.investopedia.com/terms/l/lawofdiminishingmarginalreturn.asp) applies. Quite frankly, [not every task is worth automating](https://youtube.com/shorts/_sB57-lwH9o?si=pl9l_bx-Dwwkr6p2).

I want to emphasise this is the case for the highest-value white-collar tasks, which is what OpenAI and consorts typically talk about. We have not talked about the **vast** amount of human labour which has no economic value, in the classic sense.

Beyond white-collar work, what Western countries typically talk about next is blue-collar work. [As the Michigan Journal of Economics puts it](https://sites.lsa.umich.edu/mje/2026/03/13/ai-on-the-job-industry-how-blue-collar-and-white-collar-workers-are-impacted/):

> workers in hands-on roles are not at immediate risk for job displacement due to large language models

When inevitably physical AI arrives some day, the laws of diminishing returns will apply as well. Many menial tasks have no immediate economic value at all (e.g: putting a ladder up against a wall to access a roof), but they are **essential** for some jobs. They’re also **hard** to train for, because of the variety of scenarios typically present. Physical AI is orders of magnitude harder than the well-defined problems we encounter in white-collar work.

Putting these concerns aside, we will now look at the **vast** amount of human labour that exists today: the informal economy.
The [International Monetary Fund estimates estimates](https://www.imf.org/en/publications/fandd/issues/2020/12/what-is-the-informal-economy-basics):

> about 2 billion workers, or 60 percent of the world’s employed population ages 15 and older, spend at least part of their time in the informal sector

Let that roll off your tongue, again. 60% of the working population works in the informal economy.
This kind of work encompasses everything from sustenance-farming to your neighbours kid mowing your lawn at 3pm on Sunday.

This is work that AI companies **can’t** capture, at all. Economically speaking, there is no demand. If there is no demand, investors can’t give you money. It's pretty straightforward.

Beyond the informal economy there is even more work that currently has no economic reward model at all. Emotional labour and _”soft skills”_ (talking to and caring about people) are essential for many groups of workers (__especially__ high-value jobs such as managers). These skills usually come _”packaged”_ with a certain role and is socially rewarded (nurses, restaurant staff, managers) etc. You are unlikely to retain your job if you fail to adhere to this social expectation (e.g: being rude). No specification exists for this work either.

Even if we wanted to create **EverythingAI**, we will run into a lot of work that is not well-defined, and has no economic leverage to become defined by experts. We would need to be extraordinarily showered with money, no questions asked, for many decades, to have even the slightest chance of specifying some of it.

## No one is infallible to groupthink

If you’re reading this and are thinking: _“well, duh, isn’t this like, obvious”_? Looking at Ilya’s quote, this does not seem to be the case.

I’ll give you a digest of AI Index compiled by the [Human-Centered Artificial Intelligence group at Stanford](https://hai.stanford.edu/news/ai-index-diversity-report-unmoving-needle):

> Women account for less than 19%, on average, of all AI and computer science (CS) PhD graduates in North America over the past 10 years.

As well as:

> In 2019, 45% of new U.S.-resident AI PhD graduates were white, while 2.4% were African American and 3.2% were Hispanic.

The absolute majority of AI researchers is constituted by white (45%) and asian (30%) men between the ages of 25 and 35. Of those, almost everyone is a lifelong academic. AI researchers are essentially a close-knit cult of people who have in all likelihood never lifted a hammer, much less worked a blue-collar job.

Does it surprise you that the group AI researchers could be fallible? That they don’t understand the complexity of jobs outside their own occupation? Hardly so.

Groupthink has profound effects and has been linked to several famous disasters in history, including the [Challenger disaster](https://sites.psu.edu/aspsy/2020/10/07/how-groupthink-played-a-role-in-the-challenger-disaster/). It is not unlikely that the AI research bubble is another case of conformist groupthink.

I have written repeatedly on this blog about the [The Bitter Lesson in AI](https://www.cs.utexas.edu/~eunsol/courses/data/bitter_lesson.pdf). This paradigm has been hard-wired into every CS graduate for about the past five years. Scaling is the way forward. Of course, blindly following a single paradigm can have side-effects. [Maslow described this concept as the _”hammer”_:](https://everydayconcepts.io/maslows-hammer):

> I suppose it is tempting, if the only tool you have is a hammer, to treat everything as if it were a nail.

Next time you read an AI researcher’s forecast on their own models, and how good they are at their own benchmarks, remind yourself: a benchmark is a nail too. Reality exists and is a lot more complex than us desk-people would like to admit at first glance.

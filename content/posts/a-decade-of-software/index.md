---
title: "A decade of software"
description: "Reflections on my first decade in the profession of software engineering."
author: "Lennard Berger"
date: "2026-04-19"
categories: [softwareengineering]
---

May 2026 marks a personal milestone: getting paid to write code for one decade. It feels surreal writing this.

I thought I'd like to take the time to share my learnings, for interested readers. I'll will keep it short and talk about five key topics:

1. [Software is for humans](#software-is-for-humans)
2. [Software is your biggest liability](#software-is-your-biggest-liability)
3. [The secret to get things done, is to do them](#the-secret-to-get-things-done-is-to-do-them)
4. [Surprising things a university degree teaches you](#surprising-things-a-university-degree-teaches-you)
5. [People trump profit every time](#people-trump-profit-every-time)

I hope my whimsical headings peaked your interest, so let's dive right into it!

## Software is for humans

Sounds obvious, right? Software? For humans? Who else would we design software for.
Surprisingly enough a decent amount of time is spent translating customer needs into software. It is an entire profession on its own, with project managers, agile and all the bells and whistles.
This level of abstraction [results in varrying levels of effectiveness](https://medium.com/@thecodingteacher_52591/modern-agile-is-stupid-on-why-all-great-ideas-are-killed-by-simple-minded-idiots-why-jira-kills-02080b937de2).

The painfully obvious lessons for many developers should be the following:

- understand what the business you are working for is doing
- who are your customers and what is the unique selling point of the software you are selling
- are you (still) solving that selling point?

Everything else just doesn't matter. A dashboard that no one pays for? Doesn't matter. Buttons in yellow instead of green? Doesn't matter. 
XML exports if your client uses Apple Mail? You get the idea.

Arguably this **IS** a product managers job, but then again it isn't.

If you do not understand what your customer is trying to do, chances are, the contributions to the software are going to be crap.
This gap cannot and will not be filled by abstractions other people create for you.

One learning here is you should spend time upfront to get to know your (employers) customers, understand what they value about the product, and how you can contribute meaningfully.

## Software is your biggest liability

Software is cheap. Any good programmer can whip up a small prototype in a couple hours. The speed of this has drastically increased with LLM adoption.

As a software business, your biggest expense (for all intends and purposes) are employees, and hence hours worked.

Each line in a software has the potential to create bugs that will steal valuable time (because you have to fix it), which could have been spent elsewhere.

This is exactly why [KISS](https://en.wikipedia.org/wiki/KISS_principle) exists. In my humble opinion:

- you should build **only** prototypes and throw away 90% of your code
- the only code that is not a liability are tests 😉
- don't add things you don't need, and push back on people that want those things

More often than not people simply don't need things, or they don't need them in a way you'd think they need.

I will give you a concrete example:

1. sales agent comes in and demands a dashboard for problem XYZ
2. PM takes in that request and asks the developer to build dashboard XYZ
3. developer builds dashboard
4. sales agent comes in and demands a new dashboard, XXY with tangentially similar data

Instead of building the dashboard, why not allow a read-only data connector. Make your data store a data source in Power BI.
Any sales agent with knowledge of Excell (which is the vast majority) will be able to self-serve their initial request **AND** subsequent requests.

Avoids maintenance, frees up your time, frees up the PMs time, frees up the sales agents time (because they can quickly act instead of waiting).

You can see how additional code quickly becomes a liability where there simply isn't any need to write code to begin with.

## The secret to get things done, is to do them

The Paretto principle also applies to software engineering (no surprises here). 80% of your value comes from 20% of your time.

What's the lesson learnt here? We can spend **WEEKS** planning and specifying, and that will lead us exactly nowhere.
Chances are what you are building has nothing to do with what you planned in those meetings.

Instead, start with tests. Test-driven development exists for a reason. I know its annoying and less gratifying then writing software.
However, tests are not merely about testing software. TDD has a entirely different function as well:

- you define the behaviour of the software
- you find edge cases, and there's usually a few of them

You can start writing tests today. Start with the problems you want to solve. Write them down.

If you don't like your tests, you can throw them away (or comment them out). Slowly, iteratively, you will have created the spec you wanted to have.

In that sense, the secret recipe to get things done simply is to do them. Don't be afraid to make mistakes. You **WILL** make them.
Using TDD however, you'll have a structured approach that will yield a well-defined solution to your initial problem.

Of course, Waterfall development sometimes has merit. If you are a tenured engineer, and you want to shoot rockets to the moon, you need strict specifications.
Under such circumstances budgets are usually more lenient, and you won't have a VC squashing your project if you don't deliver within the first three months.

## Surprising things a university degree teaches you

When I started writing code as a profession, a university degree was the de-facto way to become a programmer.
Over the years [this sentiment has changed](https://www.reddit.com/r/learnprogramming/comments/1otz8ft/is_it_worth_going_to_university_to_learn/), and the hundreds of bootcamps are a testiment to the fact.

Looking back at the bootcamp movement I think the fundamental idea around universities is misunderstood.

A university's top priority is to secure funding. To secure funding, you need scientific personel. To be a scientist, you need to learn to do science.
You need to learn to do experiments with rigor. At the end of your degree, ideally, you will be able to have original hypotheses, test them and falsify them too.

Programming is only tangentially related to a Computer Science degree. Programming is useful, and is an area of study in CS, but it is one of **MANY** things to know.
What becoming a scientist really means is something that Martin Fowler has spelled out to be an [expert generalist](https://martinfowler.com/articles/expert-generalist.html).

Someone who has a broad interest in **MANY** different things, strong foundational and mathematical understanding, and the knowledge to follow through with the rigor of an engineer.
Tangentially, this skill is also usefull as a programmer, if you want to earn a living.

I have always found the notion of a _"Python programmer"_ or a _"Frontend Developer"_ to be a bit quirky.

Suppose you hired an electrician to fix your lighting. You would not hire an interior & light electrician. You'd hire an electrician.

Similarly, a software engineer is someone who (given a little bit of time) can find solutions to problems in any but the most complex software projects.

It requires a lot of time and sacrifice for a lot of knowledge to be gained, but the learning here is that a university degree will (possibly) help you to think holistically about software engineering.

## People trump profit every time

I've dedicated 80% of this blog post to talk about the art of making software, but the most important 20% is why you do it.

If you come into work every day with a bad taste in your mouth, dislike your coworkers, and think your job is useless or uninteresting, it just isn't worth carrying on.

Roughly 13 years of your life will be spent in an office. 13 years continous work. Even though the economic situation isn't awesome (has it ever been?), make sure you don't numb yourself over a job. 
Likewise, if you really like a job and the people, and it keeps you interested in what you are doing, you're fine to stay put, even if you aren't paid at the far end of your salary band.

Keeping your curiosity alive is good for your spirit, and tangentially makes you more employable too.

I hope you enjoyed the bits of wisdom accrued over the past decade of software development. I'm certainly keen to see what 2036 me will think about this post 🙃.

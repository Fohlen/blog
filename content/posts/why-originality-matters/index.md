---
title: "Who wrote it first, or: why originality matters?"
description: "A perspective on the news industry and how to create more relevant news feeds for your customers."
author: "Lennard Berger"
date: "2023-06-15"
categories: [news,originality]
---

Ever since the introduction of language, humans have suffered from a fundamental problem: there is an exponentially growing amount of information, and only so much lifetime (of any individual), to grasp it. This has become an increasing problem with the advent of the World Wide Web. Individuals now have access to more information than any generation of humans, ever before, in history. However, access to more information doesn’t necessarily translate to better understanding.

At [YUKKA Lab][yukka] we are trying to solve the problem of information overload. Most notably we condense unstructured information into structured information by asking Wh-questions. Who is in the news? What have they been doing? When have they been doing it?

Structured information is useful in a variety of cases, most notably when monitoring the news for abnormalities (essentially, portfolio management).

However, structured information cannot always adequately represent individual articles. There are articles which are “just iconic” or trending and set the tone for discourse to follow for a long time to come.

When diving into the news and trending stories, we would like to show content to customers that’s __relevant__ to them.

Relevancy, however, is a difficult concept. With millions of news articles every day, what constitutes relevancy? In this blogpost we’d like to unravel some of the metrics we offer to our customers, and how it helps them to find news relevant to them.

## Relevance is a classic tale

If you’ve used news products such as Google News before, you may say: this one is easy. I want articles in my feed that are like the ones I’ve read before.

This is a standard recommender system such as it is used by Google News, and many social media platforms. If you look at an article, the platform will serve you up with similar content. The more articles you look at, the more similar the recommendations become.

At [YUKKA Lab][yukka] we have the same capability, we can use your bookmarks to recommend you articles with matching headlines. We use semantic embeddings to make this possible. It’s an easy way to filter down the news. **But** recommender systems only go so far.

What if you’d like to get news articles that are unlike the ones you have bookmarked? One can do that by recommending the opposite (articles that are unlike your bookmarks).

Attentive readers may have spotted a problem right away: this creates a filter bubble. Want articles in a different semantic space? To solve this issue, recommender systems by themselves are insufficient. If we were to create a “social-media-esque” algorithm, we would need to mix in other relevant content, such as trending news.

But recommender systems come with a plethora of problems, most notably **bias*+. The model used to create our news embedding is trained on a corpus, which has bias. Limiting the news for our customers arbitrarily using a machine learning system not only creates friction (we would need to adjust the recommendation algorithm to adjust what’s “popular”), but it would contort the view on the news.

Thankfully, we are not a social media company, and we are not primarily interested in user engagement. Instead, we want to give our users an informed, unbiased view of the news.

To do this, we’ve moved from purely recommender-based systems to a more approachable, quantitative view on what’s happening.

## Narrowing down: who reads the news

How can we use an objective, quantitative way to order and give importance to articles? The most intuitive way would be to select the most read articles. This is commonly called **readership**.

Before the advent of the internet, when we still sent telegrams across the sea, readership for printed publications could be easily calculated. You count the number of copies sold of the newspaper. Individual articles were not captured, as the publication number was what mattered. Although this didn’t consider those “secondhand readers” (your café neighbor free riding on your bought copy), nor heterogeneous reader behavior, it was consistent and comparable. With the digitization of news, however, the measure of readership has completely changed.

The most common readership metric for online publications, which is where most people get their news from, measures the number of unique visitors that click on an article (**click-based approach**). This approach is not always straightforward to measure and compare:

- The lifespan of an article on a website can be different
- Users can get the main message from an article without having clicked on it
- Cookies can lead to an overestimate by not identifying truly unique visitors
- Pay-walled news are difficult to compare
- Accessing this data can be very hard as it is the publisher’s property

A click-based readership metric objectively props up those articles that are the most read, and, arguably, have the most important information, giving the user the best possible experience. Think of the “Wisdom of the Crowd” theory, the collective wisdom and behaviour of people will result in an efficient and accurate outcome. They will be reading truthful and correct news, that everyone else is reading too and will not miss out on major news, great!

There are numerous issues with this idea, though:

- Articles from more populous regions will be inflated solely due to their demographic characteristics, and not the worldwide importance of the information. A local article about an emergency in Delhi might be read by 30 million people, it will still be completely irrelevant for much of the world
- Smaller, more niche, news might not be read, while still being important. These are moments where certain people can identify a crisis, a trend, before it happens. Wouldn’t this be a special added value, to identify news before it blows up?
- What the user is doing when reading the article can be more important than the readership number. How long does it take for them to read the article? Are they skimming over the paragraphs? Are they just looking over the title, or the images?

In combination with this click-based approach, certain source providers have used that metric to **rank** sources. Ordering them based on their website traffic. This could be a worldwide, country or category specific rank. This makes it easier to filter for the most important information in a specific geography or sector, allowing for a more personalized experience. However, this leads me to the most important question of all:

### Does readership really ensure quality, reliability, and relevance?

![Fictional example of clickbait style adverts (Lord Belbury)](./Example_clickbait_adverts.webp)

At the end of the day, it is just website traffic. It does not tell us anything about fake news, honest errors, outdated information, or poor fact checking. Click-bait titles, sensationalist topics and news that prey on people’s insecurities and ignorance can all get incredible traffic. Does that mean that article should be shown? Probably not. This really makes the case for metrics that go beyond just readership and includes other factors that enable us to assess the relevance of an article for a user.

## Beyond readership: looking at news authors

So far, we’ve introduced metrics defining readership. However, at [YUKKA Lab][yukka] we’ve come up with more ways to make news sensible. We would like to introduce two metrics of our own: **First reported** and **outreach**.

In the world of news, it is common to cite existing content to adapt it to the appropriate audience (for instance, local news outlets get their articles from larger press agencies). Original authors distribute their content via different means, such as associations (the APA for instance). Tracking the relationships between news sources is difficult however. Who wrote the article originally? Which outlet does the reporter belong to? In the print world, this was a relatively known quantity. How can we extend the same idea to into the computer age? How do we manage to account for blogs and other information sources, all while at the same not being susceptible to fake news?

To accomplish this, we track all the articles that fall into the same story (which share very similar headlines or content). By looking at the timeline of news articles, we can determine who has consistently published stories first (before other sources). To measure this, we register all articles under the same story. We then assign the first source to report on this story one point. This allows us to rank sources based on how often they publish first.

![The good news (Lizz Lunney)](./the-good-news.webp)

Sources who fall into this category report original content, attracting a lot of attention. It is no surprise that we find major news outlets such as __CBS__, __Yahoo finance__ etc. on top of this list. If we apply the same metric to a list of sources in specific geographic regions, this allows us to effectively filter down the news for original content.

Further, it is possible to build a network of citations (which journalist or outlet is cited by whom). This can be a helpful tool in determining who originally wrote a specific opinion piece. At present time we do not augment our knowledge graph with this information, but it is certainly a promising idea for future improvement.

Beyond knowing who publishes content first, we would also like to know the impact of sources. In a similar manner as we measure originality, we can track which source copies from whom. Because our rich knowledge graph contains information about the geographic origin of all our sources, we can therefore tell if sources are cited:

- regionally
- nationally
- internationally

To this end, we define outreach by clustering sources into one of these three categories (by using the majority count).
This data is useful to track specific stories that “break loose”, but it also offers us a glimpse into high quality, journalistic content. Against all odds, news outlets with high international outreach are small, independent newspapers, such as __The Grand Island Independent__.
Outreach can therefore be used to find sources targeting specific geographic areas with high impact articles. We believe this is an improvement over traditional, readership-based metrics.

## News metrics: Different windows into the world

![White framed glass window during daytime (Laura Cleffmann)](./laura-cleffmann-z3drmcczVTc-unsplash.webp)

As outlined, there are several different ways to break down the news. However, as news are as varied as their use cases, there is no “one-way-rules-it-all”-approach. In order not to obscure the view on the news, we consider many different ways to look at them.

- If you are an advertiser, you may be interested to reach the broadest possible audience. In this case, click-based readership numbers may be interesting to you
- If you operate in a more niche market, you may need to reach specific demographics. By using the first reported metric and applying a geographic filter, you will be able to reach a large number of users in a specific place
- If you are interested to break out of the usual news cycles, looking at sources with medium local outreach and high international outreach can be an excellent way to augment your usual news reads

We hope this helps understanding how news can be broken down to fit for your specific use case. If you are interested in our metrics don’t hesitate to contact us!

### Acknowledgments

Much appreciation goes to [Thomas Adler](https://medium.com/@chalk_ball) who has contributed greatly to the investigation and overall conception of this post, and to all the colleagues who have helped us along the way with constructive criticism as well as ideation.

[yukka]: https://www.yukkalab.com

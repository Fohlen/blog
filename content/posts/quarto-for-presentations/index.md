---
title: "Quarto for scientific presentations"
description: "Quarto is useful for all kinds of things, including your everyday presentations."
author: "Lennard Berger"
date: "2025-08-28"
categories: [quarto,presentations]
---

If you haven't heard about [Quarto](https://quarto.org/) yet, it self-describes as an "open-source scientific and technical publishing system".
You've certainly used Quarto - or consumed media produced by Quarto, in fact this very blog is powered by Quarto.

Quarto has some simple core ideas:

- use Markdown as a universal templating language
- make it easy to include and its output in documents
- make visualization easy (and fun)

Quarto is powerful and agnostic about the programming language and documents you want to render - it supports creating websites, documents and **presentations**.

Today we'll talk about the later - and we're not talking about fancy `RevealJS` presentations, but rather simple slideshows that you can create with minimal effort.

I'll include a step by step guide to get you started, and then we'll dive into some of the more advanced features.

## Getting started

First things first, you'll need to install Quarto - you can find the [installation instructions on their website](https://quarto.org/docs/get-started/).

Once you have Quarto installed, you can use any text editor (e.g Visual Studio Code) of your liking and create a new file with the extension `.qmd` (Quarto Markdown).
We'll call our file `presentation.qmd` and fill it with the following content:

```md
---
title: "Quarto for scientific presentations"
format: "pptx"
author: "Lennard Berger"
date: "2025-08-28"
---

## Slide 1
Welcome to your first Quarto presentation!
```

You can then render your presentation by running the following command in your terminal:

```bash
quarto render presentation.qmd
```

Congratulations - you created your first Quarto presentation! 

From now on you'll have all of the power of Markdown at your fingertips, allowing you to quickly type down your presentations. Markdown itself brings already includes a lot of features, it is best to check out the [Markdown cheatsheet](https://github.com/adam-p/markdown-here/wiki/markdown-cheatsheet).

## Power features

However, it wouldn't be a Quarto presentations if we didn't use some of its more advanced features:

```md
## Slide 2

What's the result of $y = mx + b$ when $m=2$, $x=3$ and $b=4$?
```

You can include LaTeX equations in your slides, which is especially useful for scientific presentations.

You can also [include code](https://quarto.org/docs/output-formats/html-code.html#executable-blocks):

```md
## Slide 3

python
for i in range(3):
    print(i)

```

Which will be executed and rendered - a good way to include your visualizations.

Quarto has a lot more features and it is best to check out their [full documentation](https://quarto.org/docs/reference/formats/presentations/pptx.html#code).

## Master templates

For me to make Quarto really powerful in a corporate setting I want to be able to use my company's PowerPoint template.

Quarto supports this by using [a template directive](https://quarto.org/docs/presentations/powerpoint.html#powerpoint-templates):

```md
---
title: "Presentation"
format:
  pptx:
    reference-doc: template.pptx
---
```

One can drop in a [slide master](https://support.microsoft.com/en-us/office/what-is-a-slide-master-b9abb2a0-7aef-4257-a14e-4329c904da54) and will get high quality Quarto presentations that follow their corporate design.

## Summary

While PowerPoint is already a pretty good tool for creating presentations, Quarto adds a lot of value by allowing you to quickly type down your slides in Markdown and include code and equations.
This also allows you to version presentations with Git, making it easier to track changes and collaborate with others.

Finally the master slides is what rounds off a good tool to be able to get consistent high-quality presentations.
This is why I'm have been using Quarto for all of my presentations for several years now - and I hope it'll be useful for you as well!

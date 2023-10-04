# gt

Practice typing while reading the news!

This little project came to be because a bought a funky keyboard that forced me to partially relearn how to type. Typing random stuff is boring, so why not read the news while practicing.

This is really just a wrapper for [tt](https://github.com/lemnos/tt), so go look at that project as well.

<!-- vim-markdown-toc GFM -->

* [Setup](#setup)
* [Practicing](#practicing)
* [Plots](#plots)

<!-- vim-markdown-toc -->

## Setup

* Setup [tt](https://github.com/lemnos/tt) on your system.
* Run `poetry install` to create virtual environment.

## Practicing

> [!NOTE]
> By default this script sources a bunch of Icelandic media, you might want to comment out those urls in [types.py](./gt/types.py).

```console
$ poetry run gt --help
usage: gt [-h] [--plot] [{news,quotes,text}]

positional arguments:
  {news,quotes,text}  what kind of data to practice on [default: news]

options:
  -h, --help          show this help message and exit
  --plot              show plot for data type instead of running tt
```

## Plots

Everything you type is recorded in a `csv` file in your home directory called `~/.gt-{type}.csv`. So when you want to view your progress you can run:

```console
$ poetry run gt --plot
```

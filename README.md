# gt

Practice typing while reading the news!

This little project came to be because a bought a funky keyboard that forced me to partially relearn how to type. Typing random stuff is boring, so why not read the news while practicing.

This is really just a wrapper for [tt](https://github.com/lemnos/tt), so go look at that project as well.

<!-- vim-markdown-toc GFM -->

* [Setup](#setup)
* [Practicing](#practicing)
* [Plots](#plots)
* [Viewing test data](#viewing-test-data)

<!-- vim-markdown-toc -->

## Setup

* Setup [tt](https://github.com/lemnos/tt) on your system.
* Run `poetry install` to create virtual environment.

## Practicing

> [!NOTE]
> By default this script sources a bunch of Icelandic media, you might want to pass in `news-en` as a parameter to get rid of those.

```console
$ poetry run gt --help
usage: gt [-h] [--plot] [--no-record] [--dump] [--max-length MAX_LENGTH]
          [{news,news-en,news-no,news-is,quotes,text,code,vim,program}]

positional arguments:
  {news,news-en,news-no,news-is,quotes,text,code,vim,program}
                        what kind of data to practice on [default: news]

options:
  -h, --help            show this help message and exit
  --plot                show plot for data type instead of running tt
  --no-record           do not record data
  --dump                dump test cases to stdout and exit
  --max-length MAX_LENGTH
                        max text length for any given test [default: 250]
```

## Plots

Everything you type is recorded in a `csv` file in your home directory called `~/.gt-{type}.csv`. So when you want to view your progress you can run:

```console
$ poetry run gt --plot
```

## Viewing test data

You can make `gt` dump the test data to view it:

```
$ poetry run gt --dump | jq -r '.[].text'
```

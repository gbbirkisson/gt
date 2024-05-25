import random
import re
import string
from multiprocessing import Pool

import feedparser
from requests import get

_html_clean = re.compile("<.*?>")


def flatten(l: list[list]) -> list:
    return [item for row in l for item in row]


def remove_html_tags(s: str) -> str:
    return re.sub(_html_clean, "", s)


def remove_new_lines(s: str) -> str:
    return s.replace("\n", "")


def change_unwanted_chars(s: str) -> str:
    for o, n in [("„", '"'), ("“", '"')]:
        s = s.replace(o, n)
    return s


def random_letters(n: int) -> str:
    return "".join(random.sample(string.ascii_letters, n))


def random_repetitions(c: str, max: int) -> str:
    return "".join([c for _ in range(0, random.randint(1, max))])


def rss(url: str, merge_title: bool) -> list[dict[str, str]]:
    def _format(entry: dict[str, str], merge_title: bool) -> dict[str, str]:
        title = entry["title"]
        description = entry["description"]
        link = entry["link"]
        if merge_title:
            sep = ". "
            if title[-1] in [".", "?", "!"]:
                sep = " "
            text = sep.join([entry["title"], entry["description"]])
        else:
            text = description
        text = remove_html_tags(text)
        text = remove_new_lines(text)
        text = change_unwanted_chars(text)
        return {"text": text, "attribution": link}

    return [_format(e, merge_title) for e in feedparser.parse(url).entries]


def remote_file(url: str, r: str) -> list[dict[str, str]]:
    res = []
    for line in get(url).text.splitlines():
        if re.search(r, line):
            res.append({"text": line.strip(), "attribution": url})
    return res


def quotes(count: int) -> list[dict[str, str]]:
    res = get(f"http://api.quotable.io/quotes/random?limit={count}").json()
    return [{"text": q["content"], "attribution": q["author"]} for q in res]


def code() -> list[dict[str, str]]:
    with Pool(6) as p:
        return flatten(
            p.starmap(
                remote_file,
                [
                    [
                        "https://raw.githubusercontent.com/tokio-rs/tokio/52b29b33bb7d3098fccf6092d3be51b15a9a8d91/tokio/src/future/maybe_done.rs",
                        r"fn\s.+\(.*\)",
                    ],
                    [
                        "https://raw.githubusercontent.com/pydantic/pydantic/0e33bd050de54992266240f65292cbfa4fa36be3/pydantic/v1/main.py",
                        r"def\s.+\(.*\)",
                    ],
                ],
            )
        )


def vim() -> list[dict[str, str]]:
    cmds = []
    for a in ["c", "d", "v"]:
        for b in ["i"]:
            for c in ["w", '"', "'", "(", "[", "<", "{"]:
                if a != "v":
                    cmds.append(f"{a}{b}{c}")
                else:
                    for d in ["y", "d", "c", "p"]:
                        cmds.append(f"{a}{b}{c}{d}")

    cmds.extend(
        [
            ":wq",
            ":qa!",
            "gcc",
        ]
    )

    for _ in range(random.randint(5, 10)):
        cmds.extend(
            [
                f":%s/{random_letters(4)}/{random_letters(4)}/g",
                f"V{random_repetitions('j', 5)}:s/{random_letters(4)}/{random_letters(4)}/g",
            ]
        )

    return [{"text": t} for t in cmds]


def news_is() -> list[dict[str, str]]:
    with Pool(5) as p:
        return flatten(
            p.starmap(
                rss,
                [
                    ["https://www.mbl.is/feeds/innlent/", False],
                    ["https://www.mbl.is/feeds/erlent/", False],
                    ["https://www.mbl.is/feeds/togt/", False],
                    ["https://www.mbl.is/feeds/helst/", False],
                    ["https://www.visir.is/rss/forsida/", False],
                ],
            )
        )


def news_no() -> list[dict[str, str]]:
    with Pool(2) as p:
        return flatten(
            p.starmap(
                rss,
                [
                    ["https://www.nrk.no/toppsaker.rss", False],
                    ["https://www.vg.no/rss/feed", False],
                ],
            )
        )


def news_en() -> list[dict[str, str]]:
    with Pool(3) as p:
        return flatten(
            p.starmap(
                rss,
                [
                    # ["https://rss.nytimes.com/services/xml/rss/nyt/Europe.xml", True],
                    ["https://www.theguardian.com/world/rss", True],
                    ["http://feeds.bbci.co.uk/news/technology/rss.xml", True],
                ],
            )
        )


def news() -> list[dict[str, str]]:
    return flatten(
        [
            news_en(),
            news_is(),
        ]
    )

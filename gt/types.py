import re
from multiprocessing import Pool

import feedparser
from requests import get


def flatten(l: list[list]) -> list:
    return [item for row in l for item in row]


def rss(url: str, merge_title: bool) -> list[dict[str, str]]:
    def _format(entry: dict[str, str], merge_title: bool) -> dict[str, str]:
        if merge_title:
            text = ". ".join([entry["title"], entry["description"]])
        else:
            text = entry["description"]
        text = re.sub(r"<img.+/>\n", "", text)
        text = re.sub(r"[„|“]", '"', text)
        return {"text": text, "attribution": entry["link"]}

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
                        "https://raw.githubusercontent.com/tokio-rs/tokio/master/tokio/src/future/maybe_done.rs",
                        r"fn\s.+\(.*\)",
                    ],
                ],
            )
        )


def news() -> list[dict[str, str]]:
    with Pool(6) as p:
        return flatten(
            p.starmap(
                rss,
                [
                    ["https://www.mbl.is/feeds/innlent/", False],
                    ["https://www.mbl.is/feeds/erlent/", False],
                    ["https://www.mbl.is/feeds/togt/", False],
                    ["https://www.mbl.is/feeds/helst/", False],
                    ["https://www.visir.is/rss/forsida/", False],
                    ["http://feeds.bbci.co.uk/news/technology/rss.xml", True],
                ],
            )
        )

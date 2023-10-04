import argparse

from gt.tt import plot, tt
from gt.types import code, flatten, news, quotes


def setup(t: str) -> list[dict[str, str]]:
    if t == "news":
        return news()
    if t == "quotes":
        return quotes(100)
    if t == "text":
        return flatten(
            [
                news(),
                quotes(50),
            ]
        )
    if t == "code":
        return code()

    assert False, f"'{t}' not a valid type"


def filter(entries: list[dict[str, str]]):
    return [e for e in entries if len(e["text"]) < 250]


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        nargs="?",
        choices=["news", "quotes", "text", "code"],
        default="news",
        help="what kind of data to practice on [default: news]",
    )
    parser.add_argument(
        "--plot",
        default=False,
        action="store_true",
        help="show plot for data type instead of running tt",
    )
    args = parser.parse_args()
    if args.plot:
        plot(args.type)
    else:
        tt(filter(setup(args.type)), report_name=args.type)

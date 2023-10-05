import argparse
import json
import random

from gt.tt import plot, tt
from gt.types import code, flatten, news, news_en, news_is, news_no, quotes, vim


def setup(t: str) -> list[dict[str, str]]:
    if t == "news":
        return news()
    if t == "news-en":
        return news_en()
    if t == "news-is":
        return news_is()
    if t == "news-no":
        return news_no()
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
    if t == "vim":
        return vim()
    if t == "program":
        return flatten(
            [
                vim(),
                code(),
            ]
        )

    assert False, f"'{t}' not a valid type"


def filter(entries: list[dict[str, str]], max_length: int) -> list[dict[str, str]]:
    return [e for e in entries if len(e["text"]) <= max_length]


def run() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "type",
        nargs="?",
        choices=[
            "news",
            "news-en",
            "news-no",
            "news-is",
            "quotes",
            "text",
            "code",
            "vim",
            "program",
        ],
        default="news",
        help="what kind of data to practice on [default: news]",
    )
    parser.add_argument(
        "--plot",
        default=False,
        action="store_true",
        help="show plot for data type instead of running tt",
    )
    parser.add_argument(
        "--no-record",
        default=False,
        action="store_true",
        help="do not record data",
    )
    parser.add_argument(
        "--dump",
        default=False,
        action="store_true",
        help="dump test cases to stdout and exit",
    )
    parser.add_argument(
        "--max-length",
        default=250,
        type=int,
        help="max text length for any given test [default: 250]",
    )
    args = parser.parse_args()

    data = setup(args.type)
    data = filter(data, args.max_length)
    random.shuffle(data)

    if args.dump:
        print(json.dumps(data))
        exit(0)

    if args.no_record:
        args.report_name = None

    if args.plot:
        plot(args.type)
    else:
        tt(data, report_name=args.type)

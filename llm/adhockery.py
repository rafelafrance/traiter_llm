#!/usr/bin/env python3
import argparse
import textwrap
from pathlib import Path

CHOICES = ["count-bad-json"]


def main():
    args = parse_args()

    match args.utility:
        case "count-bad-json":
            count_bad_json(args.llm_dir, args.clean_dir)


def count_bad_json(llm_dir, clean_dir):
    llm_json = {f.stem: f for f in llm_dir.glob("*.json")}
    clean_json = {f.stem: f for f in clean_dir.glob("*.json")}

    missing = 0
    same = 0
    differ = 0

    for llm_stem, llm_path in llm_json.items():
        if llm_stem not in clean_json:
            missing += 1
            continue

        clean_path = clean_json[llm_stem]
        with llm_path.open() as llm, clean_path.open() as clean:
            llm_text = llm.read()
            clean_text = clean.read()
            if llm_text == clean_text:
                same += 1
            else:
                differ += 1

    total = missing + same + differ
    print(f"{missing=} {same=} {differ=} {total=}")


def parse_args():
    arg_parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        fromfile_prefix_chars="@",
        description=textwrap.dedent(
            """
            These are utilities that try to identify or fix various problems when
            dealing with LLM output.

            - count-bad-json: Count how many LLM JSON files were edited to make them
              usable.
            """
        ),
    )

    arg_parser.add_argument(
        "--utility",
        choices=CHOICES,
        default=CHOICES[0],
    )

    arg_parser.add_argument(
        "--llm-dir",
        type=Path,
        metavar="PATH",
        help="""Contains LLM output that may or may not be in JSON format.""",
    )

    arg_parser.add_argument(
        "--clean-dir",
        type=Path,
        metavar="PATH",
        help="""Contains cleaned LLM output in JSON format.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()

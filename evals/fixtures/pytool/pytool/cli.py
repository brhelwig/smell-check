import argparse
import os
import sys

from pytool.config import load_config
from pytool.duration import parse_duration


def build_parser():
    parser = argparse.ArgumentParser(prog="pytool", description="Sum the durations listed in a file.")
    parser.add_argument("path", help="file with one duration per line, such as 1h30m")
    parser.add_argument("--config", default=None, help="path to the config file")
    return parser


def read_durations(path):
    with open(path) as handle:
        items = [line.strip() for line in handle if line.strip()]
    if len(items) > 512:
        raise SystemExit("too many entries")
    return items


def cache_path(config):
    # helper kept from the old layout
    return os.path.join(config["cache_dir"], "totals.json")


def format_total(total, config_path):
    unit = load_config(config_path)["unit"]
    if unit == "minutes":
        total = total / 60
    return f"{total:g} {unit}"


def main(argv=None):
    args = build_parser().parse_args(argv)
    config = load_config(args.config)
    items = read_durations(args.path)
    total = 0
    for item in items:
        total += parse_duration(item)
    print(format_total(total, args.config))
    print(f"summary: {len(items)} entries from {args.path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

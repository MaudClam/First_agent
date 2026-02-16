import argparse


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="first-agent")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args(argv)

    if args.version:
        print("first-agent 0.1.0")
        return 0

    parser.print_help()
    return 0


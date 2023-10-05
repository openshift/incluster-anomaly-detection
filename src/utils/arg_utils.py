"""Helper for the argument parser."""
import argparse
import textwrap


def get_arguments(args):
    """Get arguments using argparse."""
    # Do setup for the argument parser
    parser = argparse.ArgumentParser(
        prog="python",
        description=textwrap.dedent(
            """\
        This script can be used to detect anomaly based on given metric configuration.
        Optional arguments needs to pass for anomaly_names.
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-aq",
        "--anomaly_queries",
        type=lambda s: s.lower().split(",") if s else None,
        default=None,
        help="List of Queries to detect Anomaly, "
        "it should be comma separated with query names specified into configuration YAML file.",
    )

    parsed_data = parser.parse_args(args)

    return parsed_data

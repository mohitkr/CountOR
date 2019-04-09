#!/usr/bin/env python3

import numpy as np
import argparse
import countor
from pprint import pprint


def main():
    np.seterr(all='raise')

    fmt_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=fmt_class)
    parser.add_argument('csv', type=str,
                        help='Path to the input CSV')
    args = parser.parse_args()

    pprint(countor.count_or.learnConstraintsFromCSV(args.csv))


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

import numpy as np
import argparse
import countor


def main():

    fmt_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=fmt_class)
    parser.add_argument('csv', type=str,
                        help='Path to the input CSV')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='RNG seed')
    args = parser.parse_args()

    np.seterr(all='raise')
    np.random.seed(args.seed)

    rng = np.random.RandomState(args.seed)

    print(countor.count_or.learnConstraintsFromCSV(args.csv))


if __name__ == '__main__':
    main()

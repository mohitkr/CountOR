#!/usr/bin/env python3

# TODO import countor


def main():
    import argparse

    fmt_class = argparse.ArgumentDefaultsHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=fmt_class)
    parser.add_argument('csv', type=str,
                        help='Path to the input CSV')
    parser.add_argument('-s', '--seed', type=int, default=0,
                        help='RNG seed')
    args = parser.parse_args()

    np.seterr(all='raise')
    np.set_printoptions(precision=3, linewidth=80, threshold=np.nan)
    np.random.seed(args.seed)

    rng = np.random.RandomState(args.seed)

    # TODO call countor, compute performance, print results


if __name__ == '__main__':
    main()

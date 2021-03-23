#!/usr/bin/env python3

import numpy as np
import argparse
import countor

import countor.simple_sampler as sampler



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
    learned_bounds=countor.count_or.learnConstraintsFromCSV(args.csv)
    learned_bounds = [0 if v=='' else v for v in learned_bounds]
    learned_bounds=[int(v) for v in learned_bounds]
    bounds=np.array(learned_bounds).reshape(12, 7)
    bounds=np.array([b[:-1] for b in bounds])
    print(bounds)
    sampler.generateSample(12,7,3,1,bounds,"")
    print(bounds)
    # bounds
    #
    # print(countor.count_or.learnConstraintsFromCSV(args.csv))


if __name__ == '__main__':
    main()

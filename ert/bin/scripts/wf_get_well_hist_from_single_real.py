#!/usr/bin/env python
"""
 Get last value of wopth, wwpth and wgpth
 Instead of 'last' one can input a date explicitly (make sure it exists in the data set)

 Note: unfortunately explicit date is currently NOT supported with fmu-ensemble
  --> https://github.com/equinor/fmu-ensemble/issues/74

 rnyb, Nov 2019

doc:
https://equinor.github.io/fmu-ensemble/readme.html
https://github.com/equinor/fmu-ensemble/blob/master/src/fmu/ensemble/observations.py
"""

import argparse
import os

from fmu import ensemble

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description="Get WOPTH, WWPTH and WGPTH values at given date from a single realisation",
    )
    parser.add_argument(
        "-s",
        "--scratch",
        required=True,
        help="scratch path to use,including username. Example: /scratch/troll_fmu/rnyb",
    )
    parser.add_argument("-c", "--casedir", required=True, help="name of casedir to use")
    parser.add_argument(
        "-i",
        "--iterdir",
        default="iter-0",
        help="name of iterdir to use (default=iter-0)",
    )
    parser.add_argument(
        "-r",
        "--real",
        default=0,
        help="realization number to extract data from",
    )
    parser.add_argument(
        "-d",
        "--misfitdate",
        default="last",
        help="date to use, yyyy-mm-dd (default=last)",
    )

    return parser.parse_args()



def main() -> None:
    args = parse_args()
    path = args.scratch + "/" + args.casedir + "/realization-" + str(args.real) + "/" + args.iterdir
    print("Working with ensemble: ", path)

    ens = ensemble.ScratchEnsemble("single_real", path)

    smry = ens.get_smry(column_keys=["W*PTH:*"], time_index=args.misfitdate)

    # output data to file
    filepath = args.scratch + "/" + args.casedir + "/share/misfit/"
    filename = "wopth_wwpth_wgpth_" + args.misfitdate + ".csv"

    os.makedirs(filepath, exist_ok=True)

    fout = os.path.join(filepath, filename)

    print("Writing csv file: ", fout)

    smry.to_csv(fout, index=False)

    print("Done")

if __name__ == "__main__":
    main()

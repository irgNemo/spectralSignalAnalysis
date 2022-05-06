#! /usr/bin/env python
import argparse as ap


def main():
    print("Espectral signal analysis")
    args = arg_parser()
    print(args)

def read_folder_files():
    pass

def arg_parser():
    parser = ap.ArgumentParser(description="Espectral signal analysis")
    parser.add_argument("-f", "--folder", help="Folder name where the spectral files are", required=True)
    return parser.parse_args()

if __name__ == "__main__":
    main()

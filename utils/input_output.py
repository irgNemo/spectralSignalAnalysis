#! /usr/bin/env python
import argparse as ap
import os
import pandas

def main():
    print("Spectral signal analysis")
    args = arg_parser()
    text_files = read_folder_content(args.foldername)
    dataframe_list = load_folder_csv(text_files, args.foldername)
    concatenate_signal_spectrum(dataframe_list)


def concatenate_signal_spectrum(dataframe_list:list):
    for dataframe in dataframe_list:
        print(dataframe.iloc[:, 0:])
    

def load_folder_csv(text_files: list, folder_path: str) -> list:
    dataframe_list = []
    for text_file in text_files:
        file_path = "{0}{1}".format(folder_path, text_file)
        dataframe_list.append(pandas.read_csv(file_path))
    return dataframe_list


def read_folder_content(foldername: str) -> list:
    files = os.listdir(foldername)
    return files


def arg_parser() -> ap.Namespace:
    parser = ap.ArgumentParser(description="Espectral signal analysis")
    parser.add_argument("-f", "--foldername", help="Folder name where the spectral files are", required=True)
    parser.add_argument("-o", "--output", help="Output file name")
    return parser.parse_args()


if __name__ == "__main__":
    main()

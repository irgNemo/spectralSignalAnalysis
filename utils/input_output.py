#! /usr/bin/env python
import argparse as ap
import os
import pandas

def main():
    print("Spectral signal analysis")
    args = arg_parser()
    text_files = read_folder_content(args.foldername)
    dataframe_dict = load_folder_csv(text_files, args.foldername)

    for dataframe in dataframe_dict:
        dataframe.



    #spectrums_dataframe = concatenate_signal_spectrum(dataframe_dict)
    #spectrums_dataframe.to_csv(args.output,  header=True, index=False)


def concatenate_signal_spectrum(dataframes: dict) -> pandas.DataFrame:
    data = {}

    for i, key in enumerate(dataframes.keys()):
        dataframe = dataframes[key]
        column_name = "{}".format(key)
        if i == 0:
            data['wave_length'] = dataframe.iloc[:, 0:1][0].values.tolist()
        data[column_name] = dataframe.iloc[:, 1:2][1].values.tolist()

    return pandas.DataFrame(data)
    

def load_folder_csv(text_files: list, folder_path: str, header=None) -> list:
    dataframe_dict = {}
    for text_file in text_files:
        file_path = "{0}{1}".format(folder_path, text_file)
        dataframe_dict[text_file] = pandas.read_csv(file_path, header=header, delim_whitespace=True)
    return dataframe_dict


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

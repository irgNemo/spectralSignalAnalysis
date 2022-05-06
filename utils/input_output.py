#! /usr/bin/env python
import argparse as ap
import os
import pandas

def main():
    print("Spectral signal analysis")
    args = arg_parser()
    text_files = read_folder_content(args.foldername)
    
    for text_file in text_files:
        content = read_file_content(text_file)
        print(content)

def read_file_content(filename: str) -> pandas.DataFrame:
    content = pandas.read_csv(filename) 
    return content

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

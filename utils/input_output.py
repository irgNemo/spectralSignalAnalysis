#! /usr/bin/env python
import argparse as ap
import os
import pandas
import matplotlib.pyplot as plt


def plotting_boxplot(spectrums: pandas.DataFrame, filename: str, extension: str = "png", figsize: tuple = (6, 8), dpi: int = 100):
    myFig = plt.figure(figsize=figsize)
    filename = "{filename}_boxplot.{extension}".format(filename=filename, extension=extension)
    bp = spectrums.boxplot(column=spectrums.columns.values[1:].tolist())
    myFig.savefig(filename, format=extension, dpi=dpi)
    plt.close(myFig)


def plotting_all_spectrums(spectrums: dict, filename: str, extension: str = "png", figsize: tuple = (6, 8), dpi: int = 100, output_folder: str = None):
    plt.rcParams['figure.figsize'] = figsize
    columns_name = None
    for key in spectrums.keys():
         spectrum = spectrums[key]
         columns_name = spectrum.columns.values
         plt.plot(spectrum[columns_name[1]], linewidth=2, label=key)

    plt.xlabel(columns_name[0], fontsize=20)
    plt.ylabel(columns_name[1], fontsize=20)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.legend(fontsize=16, bbox_to_anchor=(1.10, 1), loc='upper right')

    if output_folder is None:
        plt.show()
    else:
        figure_save_path = "{folder}/{filename}.{extension}".format(folder=output_folder, filename=filename, extension= extension)
        plt.savefig(figure_save_path, dpi=dpi)
    plt.close()


def plotting_one_spectrum(spectrum: pandas.DataFrame, filename: str, extension:str = "png", figsize: tuple = (6, 8), dpi: int = 100, output_folder: str = None):
    columns_name = spectrum.columns.values
    fig, ax = plt.subplots(figsize=figsize)
    fig.suptitle(filename)
    ax.plot(spectrum[columns_name[0]], spectrum[columns_name[1]])
    ax.set(xlabel=columns_name[0], ylabel=columns_name[1])
    plt.draw()
    figure_save_path = "{folder}/{filename}.{extension}".format(folder=output_folder, filename=filename, extension=extension)
    fig.savefig(figure_save_path, dpi=dpi)
    plt.close(fig)


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
    parser.add_argument("-i", "--input_folder", help="Folder name where the spectral files are", required=True)
    parser.add_argument("-o", "--output_file", help="Output file name")
    parser.add_argument("-f", "--output_folder_figures", help="Output folder figures")
    return parser.parse_args()

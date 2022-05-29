"""Read and write functions from different sources

This module contains function to read input data from different sources.
Also, it has function to write information in differents formats, text
or images.
"""
import argparse as ap
import os
import pandas
import matplotlib.pyplot as plt

COLORS = ["#000000", "#00FF00", "#0000FF", "#FF0000", "#01FFFE", "#FFA6FE", "#FFDB66", "#006401", "#010067", "#95003A", "#007DB5", "#FF00F6", "#774D00", "#90FB92", "#0076FF", "#D5FF00", "#FF937E", "#6A826C", "#FF029D", "#FE8900", "#7A4782", "#7E2DD2", "#85A900", "#FF0056", "#A42400", "#00AE7E", "#683D3B", "#BDC6FF", "#263400", "#BDD393", "#00B917", "#9E008E", "#001544", "#C28C9F", "#FF74A3", "#01D0FF", "#004754", "#E56FFE", "#788231", "#0E4CA1", "#91D0CB", "#BE9970", "#968AE8", "#BB8800", "#43002C", "#DEFF74", "#00FFC6", "#FFE502", "#620E00", "#008F9C", "#98FF52", "#7544B1", "#B500FF", "#00FF78", "#FF6E41", "#005F39", "#6B6882", "#5FAD4E", "#A75740", "#A5FFD2", "#FFB167", "#009BFF", "#E85EBE"]


def plotting_boxplot(spectrums: pandas.DataFrame, output_folder_path: str, filename: str, extension: str = "png", figsize: tuple = (6, 8), dpi: int = 100):

    create_path_if_not_exist(output_folder_path)

    myFig = plt.figure(figsize=figsize)
    path = os.path.join(output_folder_path, filename)
    filename = "{path}_boxplot.{extension}".format(path=path, extension=extension)
    bp = spectrums.boxplot(column=spectrums.columns.values[1:].tolist())
    myFig.savefig(filename, format=extension, dpi=dpi)
    plt.close(myFig)


def plotting_all_spectrums(spectrums: dict, extension: str = "png", fig_size: tuple = (6, 8),
                           dpi: int = 100, output_folder: str = None):
    create_path_if_not_exist(output_folder)

    for key in spectrums.keys():
        spectrum = spectrums[key]
        plotting_one_spectrum(spectrum, key, extension, fig_size, dpi, output_folder)


def plotting_spectrums_all_together(spectrums: dict, filename: str, extension: str = "png", fig_size: tuple = (6, 8),
                           dpi: int = 100, output_folder: str = None):

    create_path_if_not_exist(output_folder)

    fig, ax = plt.subplots(figsize=fig_size)
    fig.suptitle(filename)

    for i, key in enumerate(spectrums.keys()):
        spectrum = spectrums[key]
        columns_name = spectrum.columns.values
        ax.plot(spectrum[columns_name[1]], linewidth=2, label=key, color=COLORS[i])
        ax.set(xlabel=columns_name[0], ylabel=columns_name[1])
        plt.draw()

    ax.legend(fontsize=16, bbox_to_anchor=(1.10, 1), loc='upper right')

    filename = "{}.{}".format(filename, extension)
    figure_save_path = os.path.join(output_folder, filename)
    fig.savefig(figure_save_path, dpi=dpi)
    plt.close(fig)


def plotting_one_spectrum(spectrum: pandas.DataFrame, filename: str, extension:str = "png", fig_size: tuple = (6, 8),
                          dpi: int = 100, output_folder: str = None):
    columns_name = spectrum.columns.values
    fig, ax = plt.subplots(figsize=fig_size)
    fig.suptitle(filename)
    ax.plot(spectrum[columns_name[0]], spectrum[columns_name[1]])
    ax.set(xlabel=columns_name[0], ylabel=columns_name[1])
    plt.draw()

    filename = "{filename}.{extension}".format(filename=filename, extension=extension)
    figure_save_path = os.path.join(output_folder, filename)
    fig.savefig(figure_save_path, dpi=dpi)
    plt.close(fig)


def save_dataframe_boxplot_stats(dataframe: pandas.DataFrame, output_folder_path: str, filename: str):
    create_path_if_not_exist(output_folder_path)
    output_folder_path = os.path.join(output_folder_path, filename)
    dataframe.to_csv("{}_boxplot_stats.csv".format(output_folder_path), header=True, index=True)


def save_dataframe(dataframe: pandas.DataFrame, output_folder_path: str, filename: str):
    #  Save concatenated DataFrame of the spectrums in different files
    create_path_if_not_exist(output_folder_path)
    concatenated_spectrum_filename = "{}_{}".format(filename, "concatenated_spectrums.csv")
    concatenated_spectrum_path = os.path.join(output_folder_path, concatenated_spectrum_filename)
    dataframe.to_csv(concatenated_spectrum_path, header=True, index=False)


def create_path_if_not_exist(output_folder_path: str):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)


def load_folder_csv(text_files: list, folder_path: str, header=None) -> list:
    dataframe_dict = {}
    for text_file in text_files:
        file_path = "{0}{1}".format(folder_path, text_file)
        dataframe_dict[text_file] = pandas.read_csv(file_path, header=header, delim_whitespace=True)
    return dataframe_dict


def read_folder_content(folder_name: str) -> list:
    files = os.listdir(folder_name)
    return files


def arg_parser() -> ap.Namespace:
    """Parse the command execution to obtain the arguments

    Parameters
    __________

    input_folder: str
        The path to the forlder where the files to be processed reside.

    output_file: str
        The filename (including path) where the spectral signals statistics will be written

    output_folder_figures: str
        The folder path where the images will be saved

    
    Returns
    -------
        argumentParser.Namespace
            The argumentParse namespace where the input arguments are stored
    """
    parser = ap.ArgumentParser(description="Spectral signal analysis")
    parser.add_argument("-i", "--input_folder", help="Path and folder name where the spectral files reside",
                        required=True)
    parser.add_argument("-o", "--output_folder_path", help="Path where all data will be saved")
    #parser.add_argument("-f", "--output_folder_images", help="The path to the folder where the images will be  saved")
    return parser.parse_args()

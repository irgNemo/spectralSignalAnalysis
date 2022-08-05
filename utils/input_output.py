"""Read and write functions from different sources

This module contains function to read input data from different sources.
Also, it has function to write information in different formats, text
or images.
"""
import argparse as ap
import os
import pandas
import matplotlib.pyplot as plt
import numpy as np
from utils import utils
import math

COLORS = ["#000000", "#00FF00", "#0000FF", "#FF0000", "#01FFFE", "#FFA6FE", "#FFDB66", "#006401", "#010067", "#95003A",
          "#007DB5", "#FF00F6", "#774D00", "#90FB92", "#0076FF", "#D5FF00", "#FF937E", "#6A826C", "#FF029D", "#FE8900",
          "#7A4782", "#7E2DD2", "#85A900", "#FF0056", "#A42400", "#00AE7E", "#683D3B", "#BDC6FF", "#263400", "#BDD393",
          "#00B917", "#9E008E", "#001544", "#C28C9F", "#FF74A3", "#01D0FF", "#004754", "#E56FFE", "#788231", "#0E4CA1",
          "#91D0CB", "#BE9970", "#968AE8", "#BB8800", "#43002C", "#DEFF74", "#00FFC6", "#FFE502", "#620E00", "#008F9C",
          "#98FF52", "#7544B1", "#B500FF", "#00FF78", "#FF6E41", "#005F39", "#6B6882", "#5FAD4E", "#A75740", "#A5FFD2",
          "#FFB167", "#009BFF", "#E85EBE"]


def plotting_boxplot_by_class_per_window(dataset: pandas.DataFrame, window_size: int, output_folder_path: str,
                                         folder_name: str = "boxplot_by_class\\", figsize: tuple = (40, 20),
                                         dpi: int = 200):
    # TODO Falta plotear la última parte del dataset ya que redonde hacia abajo y si no es múltiplo entonces queda sin plotear
    path = os.path.join(output_folder_path, folder_name)
    utils.create_path_if_not_exist(path)

    column_names_list = dataset.columns.values
    column_class_name = dataset.columns.values[-1]
    num_columns = len(dataset.columns) - 1

    # Calculate the number of images and layout
    #window_size = 100
    num_iterations = math.floor(num_columns / window_size)

    for i in range(num_iterations):
        window_init_index = window_size * i
        dataset_segment = list(column_names_list[window_init_index: window_init_index + window_size])
        boxplot_axes = dataset.boxplot(column=dataset_segment, by=column_class_name, figsize=figsize)

        for row in boxplot_axes:
            for axe in row:
                axe.plot()

        fig = axe.get_figure()
        figure_name = "{0}.png".format(i)
        fig.savefig(os.path.join(path, figure_name), dpi=dpi)


def plotting_boxplot(spectrums: pandas.DataFrame, output_folder_path: str, filename: str, extension: str = "png",
                     figsize: tuple = (6, 8), dpi: int = 100):
    """Plots the boxplots of the spectums in a dataframe. The plot is saved in a particular folder, in the image format
    specified bye the user.

    Parameters
    ----------
    spectrums : Dataframe with the data corresponding to several spectrums. One spectrum per column. The first column
    corresponds to the wavelength, and the additional to the reflectance
    output_folder_path : The folder path where the data will be stored
    filename : The name of the image file that contains the boxplot
    extension : The extension of the image to be saved
    figsize : The size, in inches, of the image
    dpi : The quality of the image to be save

    Returns
    -------

    """

    utils.create_path_if_not_exist(output_folder_path)

    my_fig = plt.figure(figsize=figsize)
    path = os.path.join(output_folder_path, filename)
    filename = "{path}_boxplot.{extension}".format(path=path, extension=extension)
    bp = spectrums.boxplot(column=spectrums.columns.values[1:].tolist())
    my_fig.savefig(filename, format=extension, dpi=dpi)
    plt.close(my_fig)


def plotting_all_spectrums(spectrums: dict, output_folder: str, extension: str = "png", fig_size: tuple = (6, 8),
                           dpi: int = 100):
    """This function iterate over a dictionary with all the spectrums

    Parameters
    ----------
    spectrums : A dictionary with the name and specturm pair (name -> specturm). The first column of the dataframe
    corresponds to the wavelength and the second columns to the reflectance
    extension : The extension of the image to be saved
    fig_size : The size, in inches, of the image
    dpi : The quality of the image to be save
    output_folder : The folder path where the data will be stored.

    Returns
    -------

    """
    utils.create_path_if_not_exist(output_folder)

    for key in spectrums.keys():
        spectrum = spectrums[key]
        plotting_one_spectrum(spectrum, key, extension, fig_size, dpi, output_folder)


def plotting_spectrums_all_together(spectrums: dict, filename: str, extension: str = "png", fig_size: tuple = (6, 8),
                           dpi: int = 100, output_folder: str = None):
    """This function plots all the spectrums in one image

    Parameters
    ----------
    spectrums : A dataframe with the data of several spectrums. The firs column corresponds to the wavelength while the
    rest are the reflectance of each spectrum
    filename : The name of the image to be created
    extension : The extension of the image to be created
    fig_size : The size of the figure in inches
    dpi : The quality of the image
    output_folder : The file path and folder name where the image will be stored

    Returns
    -------

    """

    utils.create_path_if_not_exist(output_folder)

    fig, ax = plt.subplots(figsize=fig_size)
    fig.suptitle(filename)
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0


    for i, key in enumerate(spectrums.keys()):
        spectrum = spectrums[key]
        columns_name = spectrum.columns.values
        x = spectrum[columns_name[0]]
        y = spectrum[columns_name[1]]
        min_x = x.min() if min_x < x.min() else min_x
        max_x = x.max() if max_x < x.max() else max_x
        min_y = y.min() if min_y < y.min() else min_y
        max_y = y.max() if max_y < y.max() else max_y
        ax.plot(x, y, linewidth=2, label=key, color=COLORS[i])
        ax.set(xlabel=columns_name[0], ylabel=columns_name[1])
        plt.draw()

    step_x = round((max_x - min_x) * 0.1)
    step_y = round((max_y - min_y) * 0.1)
    xticks = np.arange(min_x, max_x, step_x)
    yticks = np.arange(min_y, max_y, step_y)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.legend(fontsize=16, bbox_to_anchor=(1.10, 1), loc='upper right')
    ax.grid(color='r', linestyle='dotted', linewidth=1)

    filename = "{}.{}".format(filename, extension)
    figure_save_path = os.path.join(output_folder, filename)
    fig.savefig(figure_save_path, dpi=dpi)
    plt.close(fig)


def plotting_one_spectrum(spectrum: pandas.DataFrame, filename: str, extension:str = "png", fig_size: tuple = (6, 8),
                          dpi: int = 100, output_folder: str = None):
    """This function plots one spectrum

    Parameters
    ----------
    spectrum : A dataframe with the information of one spectrum. The first column corresponds to the wavelength while
    the second to the reflectance
    filename : The name of the image
    extension : The xtension of the image
    fig_size : The size of the image
    dpi : The quality of the image
    output_folder : The folder where the image will be saved

    Returns
    -------

    """

    columns_name = spectrum.columns.values
    fig, ax = plt.subplots(figsize=fig_size)
    fig.suptitle(filename)
    x = spectrum[columns_name[0]]
    y = spectrum[columns_name[1]]
    min_x = x.min()
    max_x = x.max()
    min_y = y.min()
    max_y = y.max()
    step_x = round((max_x - min_x) * 0.1)
    step_y = round((max_y - min_y) * 0.1)
    xticks = np.arange(min_x, max_x, step_x)
    yticks = np.arange(min_y, max_y, step_y)
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.plot(x, y, linewidth=2,)
    ax.set(xlabel=columns_name[0], ylabel=columns_name[1])
    ax.grid(color='r', linestyle='dotted', linewidth=1)

    filename = "{filename}.{extension}".format(filename=filename, extension=extension)
    figure_save_path = os.path.join(output_folder, filename)
    fig.savefig(figure_save_path, dpi=dpi)
    plt.close(fig)


def save_dataframe_boxplot_stats(dataframe: pandas.DataFrame, output_folder_path: str, filename: str):
    """ Save the boxplots statistics of a dataframe in a particular path with a particular name

    Parameters
    ----------
    dataframe : Dataframe to which the statistic will be computed and saved with a specific name and path
    output_folder_path : Path where the file will be stored
    filename : Name of the file to be saved

    Returns
    -------

    """

    utils.create_path_if_not_exist(output_folder_path)
    output_folder_path = os.path.join(output_folder_path, filename)
    dataframe.to_csv("{}_boxplot_stats.csv".format(output_folder_path), header=True, index=True)


def save_dataframe(dataframe: pandas.DataFrame, output_folder_path: str, filename: str):
    """ Save a dataframe in a specific path with an specific name

    Parameters
    ----------
    dataframe : Dataframe to be saved
    output_folder_path : Path where the dataframe will be saved
    filename : name of the file

    Returns
    -------

    """
    #  Save concatenated DataFrame of the spectrums in different files
    utils.create_path_if_not_exist(output_folder_path)
    concatenated_spectrum_filename = "{}_{}".format(filename, "concatenated_spectrums.csv")
    concatenated_spectrum_path = os.path.join(output_folder_path, concatenated_spectrum_filename)
    dataframe.to_csv(concatenated_spectrum_path, header=True, index=False)





def load_folder_csv(text_files: list, folder_path: str, header=None) -> list:
    """Create a list of dataframes based on a lists of csv files

    Parameters
    ----------
    text_files : List of csv files path/names
    folder_path : Path where the files are stored
    header : header definition for the dataframes

    Returns
    -------
    dataframe_dict: A dictionary with the dataframes corresponding to each file in the list. The keys are the filenames

    """
    dataframe_dict = {}
    for text_file in text_files:
        file_path = "{0}{1}".format(folder_path, text_file)
        dataframe_dict[text_file] = pandas.read_csv(file_path, header=header, delim_whitespace=True)
    return dataframe_dict


def read_folder_content(folder_name: str) -> list:
    """

    Parameters
    ----------
    folder_name : Folder path and name where the csv are located

    Returns
    -------
    files: A list with the filenames in the folder_name folder

    """
    files = os.listdir(folder_name)
    return files


def arg_parser() -> ap.Namespace:
    """Parse the command execution to obtain the arguments

    Parameters
    __________

    input_folder: str
        The path to the forlder where the files to be processed reside.

    output_folder_path: str
        The folder where the data will be stored

    
    Returns
    -------
        argumentParser.Namespace
            The argumentParse namespace where the input arguments are stored
    """
    parser = ap.ArgumentParser(description="Spectral signal analysis")
    parser.add_argument("-i", "--input_folder", help="Path and folder name where the spectral files reside",
                        required=True, nargs="+")
    parser.add_argument("-o", "--output_folder_path", help="Path where all data will be saved")
    return parser.parse_args()


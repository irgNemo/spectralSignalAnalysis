from utils import input_output as io
from utils import utils as utils
import os
import pandas
import matplotlib.pyplot as plt
import math


def main():
    print("Spectral signal analysis")  # System title

    # Parse input data
    args = io.arg_parser()

    # Variable definition
    data_header = ["wavelength", "reflectance"]
    input_folder_path = args.input_folder
    output_folder_path = args.output_folder_path

    dataset = create_dataset_signal_by_reflectance(input_folder_path)
    column_names = dataset.columns.values
    column_names_list = column_names.tolist()
    column_class_name = column_names[-1]

    # Calculating the number of images and layout
    layout = (10, 10)
    num_columns = len(dataset.columns) - 1
    window_size = (layout[0] * layout[1])
    num_iterations = math.ceil(num_columns / window_size)

    window_init = 0
    window_end = window_init + window_size

    for i in range(num_iterations):
        pass #TODO Iterar num_iteration veces para crear los box plots por bloques de 100 columnas

    # boxplot_axes = dataset.boxplot(column=column_names_list, by=column_class_name, figsize=(40, 20))


    """
    for row in boxplot_axes:
        for axe in row:
            axe.plot(layot=(5, 5))

    fig = axe.get_figure()
    figure_name = "{0}.png".format("prueba")
    fig.savefig(figure_name, dpi=200)
    """



def create_dataset_signal_by_reflectance(input_folder_path: list) -> pandas.DataFrame:
    """Create a data set of the spectrum where the rows are the signal spectrum and the colums are each wavelength
    sample

    Parameters
    ----------
    input_folder_path : Path where the folder to be analized are located

    Returns
    -------
    transponsed_spectrum: A dataframe with the spectrums transposed, i.e. the rows are the signals and the columns
    corresponds to the wavelength samples

    """

    dataframe_dict = {}
    class_labels = []

    for folder_path in input_folder_path:
        text_files = io.read_folder_content(folder_path)
        text_files.sort()
        class_name = folder_path.split('/')[-2]
        class_labels.extend([class_name] * len(text_files))
        dataframe_dict.update(io.load_folder_csv(text_files, folder_path))

    spectrums_dataframe = utils.concatenate_signal_spectrum(dataframe_dict)
    spectrums_dataframe.drop(0, inplace=True, axis=1)
    transposed_spectrum = spectrums_dataframe.transpose()
    transposed_spectrum["class"] = class_labels

    return transposed_spectrum


def signal_analysis(input_folder_paths: list, output_folder_path_root: str):
    """

    Parameters
    ----------
    input_folder_paths : Path to the folder where the information to be loaded is located

    output_folder_path :The path to the folder where to put all data generated

    Returns
    -------

    """

    # Variable definition
    data_header = ["wavelength", "reflectance"]


    for input_folder_path in input_folder_paths:
        folder_name = input_folder_path.split('/')[-2]  # Extract the last part of the input file to use it as a filename
        text_files = io.read_folder_content(input_folder_path)
        text_files.sort()
        dataframe_dict = io.load_folder_csv(text_files, input_folder_path)
        utils.insert_header(dataframe_dict, data_header)
        spectrums_dataframe = utils.concatenate_signal_spectrum(dataframe_dict)

        output_folder_path = os.path.join(output_folder_path_root, folder_name)

        # Saving concatenated spectrums to disk
        io.save_dataframe(spectrums_dataframe, output_folder_path, folder_name)

        # Saving boxplot statistics to disk
        io.save_dataframe_boxplot_stats(spectrums_dataframe.describe(), output_folder_path, folder_name)

        # Plotting boxplot in one image
        io.plotting_boxplot(spectrums_dataframe, output_folder_path=output_folder_path, filename=folder_name,
                            extension="png", figsize=(50, 20), dpi=200)

        # Plotting each spectrum on one image
        io.plotting_all_spectrums(spectrums=dataframe_dict, output_folder=output_folder_path, fig_size=(40, 20), dpi=200)

        # Plotting all spectrums together
        io.plotting_spectrums_all_together(dataframe_dict, filename=folder_name, output_folder=output_folder_path,
                                       fig_size=(40, 20), dpi=200, extension="png")


if __name__ == "__main__":
    main()

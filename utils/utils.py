import pandas
import os


def concatenate_signal_spectrum(dataframes: dict) -> pandas.DataFrame:
    """Concatenate the reflectance of several dataframes. Every dataframe in the dict contains two columns
    the first corresponding to the wavelength and the second to the reflectance.

    Parameters
    ----------
    dataframes : Dictionary with all tha dataframe spectrums to be concatenated

    Returns
    -------
    data: A dataframe with the first column been the wavelength and the rest the reflectance of the several spectrums

    """
    data = {}

    for i, key in enumerate(dataframes.keys()):
        dataframe = dataframes[key]
        columns_name = dataframe.columns.values

        if i == 0:
            data[columns_name[0]] = dataframe.iloc[:, 0:1][columns_name[0]].values.tolist()
        data[key] = dataframe.iloc[:, 1:2][columns_name[1]].values.tolist()

    return pandas.DataFrame(data)


def insert_header(spectrum_dict: dict, header: str):
    """

    Parameters
    ----------
    spectrum_dict : A dictionary with dataframes corresponding to an spectrum
    header : The header to be insterted in all dataframe

    Returns
    -------

    """
    for key in spectrum_dict.keys():
        spectrum = spectrum_dict[key]
        spectrum.columns = header


def create_path_if_not_exist(output_folder_path: str):
    """Create a particular folder tree if not exist

    Parameters
    ----------
    output_folder_path : Folder path

    Returns
    -------

    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
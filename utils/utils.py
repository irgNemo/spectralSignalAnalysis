import pandas


def concatenate_signal_spectrum(dataframes: dict) -> pandas.DataFrame:
    data = {}

    for i, key in enumerate(dataframes.keys()):
        dataframe = dataframes[key]
        columns_name = dataframe.columns.values
        # column_name = "{}".format(key)
        if i == 0:
            data[columns_name[0]] = dataframe.iloc[:, 0:1][columns_name[0]].values.tolist()
        data[key] = dataframe.iloc[:, 1:2][columns_name[1]].values.tolist()

    return pandas.DataFrame(data)


def insert_header(spectrum_dict: dict, header: str):
    for key in spectrum_dict.keys():
        spectrum = spectrum_dict[key]
        spectrum.columns = header

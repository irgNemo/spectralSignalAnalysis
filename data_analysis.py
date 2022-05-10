from utils import input_output as io
from utils import utils as utils


def main():
    print("Spectral signal analysis")
    data_header = ["wavelength", "reflectance"]
    args = io.arg_parser()

    folder_path = args.input_folder
    folder_name = folder_path.split('/')[-2]
    figure_save_path = args.output_folder_figures

    text_files = io.read_folder_content(folder_path)
    dataframe_dict = io.load_folder_csv(text_files, folder_path)
    utils.insert_header(dataframe_dict, data_header)
    spectrums_dataframe = utils.concatenate_signal_spectrum(dataframe_dict)

    spectrum_stats = spectrums_dataframe.describe()
    #spectrum_stats.to_csv("{}_boxplot_stats.csv".format(folder_name), header=True, index=True)


    #spectrums_dataframe.to_csv(args.output_file, header=True, index=False)
    #io.plotting_boxplot(spectrums_dataframe, filename=folder_name, extension="png", figsize=(50, 20), dpi=200)
    #io.plotting_all_spectrums(spectrums=dataframe_dict, filename=folder_name, output_folder=figure_save_path, figsize=(40, 20), dpi=200)

    #for key in dataframe_dict.keys():
    #    spectrum = dataframe_dict[key]
    #    io.plotting_one_spectrum(spectrum=spectrum, filename=key, output_folder=figure_save_path, extension="png", figsize=(30, 9), dpi=200)



if __name__ == "__main__":
    main()

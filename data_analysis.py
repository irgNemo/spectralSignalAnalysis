from utils import input_output as io
from utils import utils as utils
import os


def main():
    print("Spectral signal analysis") # System title

    # Parse input data
    args = io.arg_parser()

    # Variable definition
    data_header = ["wavelength", "reflectance"]
    input_folder_path = args.input_folder
    output_folder_path = args.output_folder_path
    folder_name = input_folder_path.split('/')[-2]  # Extract the last part of the input file to use it as a filename
    #  images_save_path = args.output_folder_images

    text_files = io.read_folder_content(input_folder_path)
    dataframe_dict = io.load_folder_csv(text_files, input_folder_path)
    utils.insert_header(dataframe_dict, data_header)
    spectrums_dataframe = utils.concatenate_signal_spectrum(dataframe_dict)

    output_folder_path = os.path.join(output_folder_path, folder_name)

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

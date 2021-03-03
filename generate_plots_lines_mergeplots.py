import matplotlib.pyplot as plt


from read_excel_and_extract_data import read_excel_from_dir,\
    read_sample_creator, read_sml, read_which_are_acrylates_and_pi

excel_dir = r"C:\Users\sebero\PycharmProjects\analysispdfcreator\Migration samples results.xlsx"


def create_subplots(excel_dir):
    df = read_excel_from_dir(excel_dir)
    dict_pi_acr = read_which_are_acrylates_and_pi(df)
    value_iterator = iter(dict_pi_acr)
    acrylates = next(value_iterator)
    photoinitiators = next(value_iterator)
    person_dict = read_sample_creator(df)
    sml = read_sml(df)

    values = sml.values()
    sml_list_acry = list(values)[0:photoinitiators-acrylates]
    sml_list_pic = list(values)[photoinitiators-2:]

    for row in range(3, df.shape[0]):
        list_of_y_acry = []
        list_of_x_acry = []
        list_of_y_pic = []
        list_of_x_pic = []
        counter = 0
        person = person_dict[row+2]
        list_of_colors_acry = []
        list_of_colors_pic = []
        failed_migration_acry = False
        failed_migration_pic = False

        for col_acry in range(2, photoinitiators):
            list_of_x_acry.append(df.iloc[0, col_acry].replace(" (ppb)", ""))
            if str(df.iloc[row, col_acry]) == "ND":
                list_of_y_acry.append(0)
            else:
                list_of_y_acry.append(int(df.iloc[row, col_acry]))

            if list_of_y_acry[counter] > sml_list_acry[counter]:
                list_of_colors_acry.append("red")
                failed_migration_acry = True
            else:
                list_of_colors_acry.append("green")

            counter += 1

        counter = 0
        for col_pic in range(photoinitiators, df.shape[1]):
            list_of_x_pic.append(df.iloc[0, col_pic].replace(" (ppb)", ""))
            if str(df.iloc[row, col_pic]) == "ND":
                list_of_y_pic.append(0)
            else:
                list_of_y_pic.append(int(df.iloc[row, col_pic]))
            if list_of_y_pic[counter] > sml_list_pic[counter]:
                list_of_colors_pic.append("red")
                failed_migration_pic = True
            else:
                list_of_colors_pic.append("green")
            counter += 1

        len_acry = range(len(list_of_x_acry))
        len_pic = range(len(list_of_x_pic))

        acrylates_masked_list = []
        pic_masked_list = []

        for n in len_acry:
            string = f"Acrylate {n+1}"
            acrylates_masked_list.append(string)

        for n in len_pic:
            string = f"Photoinitiator {n+1}"
            pic_masked_list.append(string)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        x1, y1 = [-0.5, 3.5], [50, 50]
        x2, y2 = [3.5, 10.5], [10, 10]
        x3, y3 = [-0.5, 6.5], [50, 50]
        x4, y4 = [6.5, 10.5], [10, 10]

        ax1.bar(list_of_x_acry, list_of_y_acry, color=list_of_colors_acry, align='center')
        ax2.bar(list_of_x_pic, list_of_y_pic, color=list_of_colors_pic, align='center')

        ax1.plot(x1, y1, marker='o', ls="--", c="k")
        ax1.plot(x2, y2, marker='o', ls="--", c="k")
        ax2.plot(x3, y3, marker='o', ls="--", c="k")
        ax2.plot(x4, y4, marker='o', ls="--", c="k")

        fig.suptitle("Sample id: " + str(df.iloc[row, 0]), fontsize=20)
        ax1.set_xticklabels(acrylates_masked_list, rotation=90)
        ax1.set_ylabel("Migration [ppb]")

        ax2.set_xticklabels(pic_masked_list, rotation=90)
        ax2.set_ylabel("Migration [ppb]")

        b1, = ax1.plot([], marker="s", markersize=15, linestyle="", color="g",  label="Passed migration")
        b2, = ax1.plot([], markersize=15, linestyle="--", color="k",  label="Migration Limit")

        b4, = ax2.plot([], marker="s", markersize=15, linestyle="", color="g",  label="Passed migration")
        b5, = ax2.plot([], markersize=15, linestyle="--", color="k",  label="Migration Limit")

        if failed_migration_acry:
            b3, = ax1.plot([], marker="s", markersize=15, linestyle="", color="r",  label="Failed migration")
            ax1.legend(handles=[b1, b3, b2])
        else:
            ax1.legend(handles=[b1, b2])

        if failed_migration_pic:
            b6, = ax2.plot([], marker="s", markersize=15, linestyle="", color="r",  label="Failed migration")
            ax2.legend(handles=[b4, b6, b5])
        else:
            ax2.legend(handles=[b4, b5])

        plt.tight_layout()
        plt.savefig("plot_folder/migration_image_" + person + "_sample_id_" + str(df.iloc[row, 0]), bbox_inches='tight')
        plt.close()

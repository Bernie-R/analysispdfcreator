import matplotlib.pyplot as plt
import os
import numpy as np


from read_excel_and_extract_data import read_excel_from_dir, read_a_and_p, read_sample_id, read_sample_creator, read_cas, read_sml, read_which_are_acrylates_and_pi

#dir = r"C:\Users\sebero\PycharmProjects\analysispdfcreator\Migration samples results.xlsx"

def create_plot_acrylates(dir):
    df = read_excel_from_dir(dir)
    dict = read_which_are_acrylates_and_pi(df)
    value_iterator = iter(dict)
    Acrylates = next(value_iterator)
    Photoinitiators = next(value_iterator)
    person_dict = read_sample_creator(df)
    sml = read_sml(df)
    values = sml.values()
    sml_list = list(values)[0:Photoinitiators-Acrylates]

    for row in range(3,df.shape[0]):
        list_of_y = []
        list_of_x = []
        counter = 0
        person = person_dict[row+2]
        list_of_colors = []
        failed_migration = False
        for col in range(2, Photoinitiators):

            list_of_x.append(df.iloc[0,col].replace(" (ppb)", ""))
            if str(df.iloc[row,col]) == "ND":
                list_of_y.append(0)
            else:
                list_of_y.append(int(df.iloc[row,col]))
            if list_of_y[counter] > sml_list[counter]:
                list_of_colors.append("red")
                failed_migration = True
            else:
                list_of_colors.append("green")
            counter += 1
        #plotting
        ax = plt.subplot(111)

        #x1, y1 = [0, 50], [0, 50]
        #x2, y2 = [0, 50], [0, 50]
        #plt.plot(x1, y1, x2, y2, marker = 'o')

        ax.bar(list_of_x, sml_list, width=0.5, color='lightgray', align='center')
        ax.bar(list_of_x, list_of_y, width=0.2, color=list_of_colors, align='center')
        plt.xticks(list_of_x, rotation='vertical')
        plt.ylabel("Migration [ppb]")
        b1, =ax.plot([], marker="s", markersize=15, linestyle="", color="lightgray",  label="Migration Limit")
        b2, =ax.plot([], marker="s", markersize=15, linestyle="", color="g",  label="Passed migration")
        if failed_migration == True:
            b3, =ax.plot([], marker="s", markersize=15, linestyle="", color="r",  label="Failed migration")
            ax.legend(handles=[b1, b2, b3])
        else:
            ax.legend(handles=[b1, b2])
        plt.tight_layout()
        plt.title("Acrylate Migration - Sample ID: " + str(df.iloc[row,0]))
        if not os.path.exists('plot_folder'):
            os.makedirs('plot_folder')
        #ax.figure.set_size_inches(10, 8)
        plt.savefig("plot_folder/acrylate_temp_" + person + "_sample_id_" + str(df.iloc[row,0]), bbox_inches='tight', )
        plt.clf()

create_plot_acrylates(r"C:\Users\sebero\PycharmProjects\analysispdfcreator\Migration samples results.xlsx")


def create_plot_photoinitiators(dir):
    df = read_excel_from_dir(dir)
    dict = read_which_are_acrylates_and_pi(df)
    value_iterator = iter(dict)
    Acrylates = next(value_iterator)
    Photoinitiators = next(value_iterator)
    person_dict = read_sample_creator(df)
    sml = read_sml(df)
    values = sml.values()
    sml_list = list(values)[Photoinitiators-2:]


    for row in range(3,df.shape[0]):
            list_of_y = []
            list_of_x = []
            counter = 0
            person = person_dict[row+2]
            list_of_colors = []
            failed_migration = False
            for col in range(Photoinitiators, df.shape[1]):

                list_of_x.append(df.iloc[0,col].replace(" (ppb)", ""))
                if str(df.iloc[row,col]) == "ND":
                    list_of_y.append(0)
                else:
                    list_of_y.append(int(df.iloc[row,col]))
                if list_of_y[counter] > sml_list[counter]:
                    list_of_colors.append("red")
                    failed_migration = True
                else:
                    list_of_colors.append("green")
                counter += 1

            #plotting
            ax = plt.subplot(111)
            ax.bar(list_of_x, sml_list, width=0.5, color='lightgray', align='center')
            ax.bar(list_of_x, list_of_y, width=0.2, color=list_of_colors, align='center')
            plt.xticks(list_of_x, rotation='vertical')
            plt.ylabel("Migration [ppb]")
            b1, =ax.plot([], marker="s", markersize=15, linestyle="", color="lightgray",  label="Migration Limit")
            b2, =ax.plot([], marker="s", markersize=15, linestyle="", color="g",  label="Passed migration")
            if failed_migration == True:
                b3, =ax.plot([], marker="s", markersize=15, linestyle="", color="r",  label="Failed migration")
                ax.legend(handles=[b1, b2, b3])
            else:
                ax.legend(handles=[b1, b2])
            plt.tight_layout()
            plt.title("Photoinitiator Migration - Sample ID: " + str(df.iloc[row,0]))
            if not os.path.exists('plot_folder'):
                os.makedirs('plot_folder')
            plt.savefig("plot_folder/photoinitiator_temp_" + person + "_sample_id_" + str(df.iloc[row,0]), bbox_inches='tight')

            plt.clf()


#create_plot_photoinitiators(dir)
#create_plot_acrylates(dir)
# Python libraries
from fpdf import FPDF
from datetime import datetime
import glob
import re
from tqdm import tqdm
import pandas as pd

from read_excel_and_extract_data import read_sample_id,\
    read_a_and_p, read_excel_from_dir, read_which_are_acrylates_and_pi, read_sml

# Local libraries
from generate_plots_lines_mergeplots import create_subplots

filename = "./output.pdf"

WIDTH = 210
HEIGHT = 297

logo_dir = "./resources/logo.jpg"


def create_title(day, pdf):
    pdf.set_font('Arial', '', 24)
    pdf.ln(10)
    pdf.write(5, f"Analytical Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(2)


def create_logo(image_dir, pdf):
    pdf.ln(10)
    pdf.image(image_dir, 150, 8, 50)


def add_contact_info(name, pdf):
    pdf.set_font('Arial', '', 8)
    pdf.write(4, "Contact Information:")
    pdf.ln(3)
    pdf.write(4, "Davide Mendes - Analytical R&D Engineer")
    pdf.ln(3)
    pdf.write(4, "Davide.Mendes@flintgrp.com")
    pdf.ln(3)
    pdf.write(4, "+46 733 379 202")
    pdf.ln(5)

    pdf.write(4, f"Sample requester: {name}")
    pdf.ln(3)


def footer(pdf):
    generate_d_t = "Report generated on: " + datetime.now().strftime('%m/%d/%Y')
    page = 'Page ' + str(pdf.page_no()) + ''

    pdf.set_y(1)
    pdf.set_font('Arial', '', 9)
    pdf.cell(5, 5, "Migration Report", 0, 0, 'L')
    pdf.cell(0, 5, page, 0, 0, 'C')
    pdf.cell(0, 5, generate_d_t, 0, 0, 'R')


def generate_legend(pdf, excel_directory):

    pdf.ln(3)
    pdf.write(4, "Legend:")
    pdf.ln(5)
    epw = pdf.w - 2*pdf.l_margin
    col_width = epw/4
    th = pdf.font_size
    df = read_excel_from_dir(excel_directory)
    dict_values = read_which_are_acrylates_and_pi(df)
    chem_data = read_a_and_p(df)
    length_data = len(chem_data)
    list_of_rows = []
    chemical_value = int(list(dict_values.items())[1][0]) - 2
    counter = 1

    for i in range(length_data):
        if counter >= chemical_value:
            list_of_rows.append([f"Photoinitiator {counter - chemical_value + 1}", chem_data[i+2]])
        else:
            list_of_rows.append([f"Acrylate {counter}", chem_data[i+2]])
        counter += 1

    for num, row in enumerate(list_of_rows, 1):
        for datum in row:
            # Enter data in colums
            pdf.cell(col_width, 2*th, str(datum), border=1)
        if num % 2 == 0:
            pdf.ln(2*th)
        length_legend = num*2
    return length_legend


def get_full_name(short_name):
    name_dict = pd.read_excel("name_dict.xlsx")
    for row, name in enumerate(name_dict["Short"]):
        if name == short_name:
            full_name = name_dict.iloc[row]['Long']
            return full_name

def create_analytics_report(excel_directory):
    create_subplots(excel_directory)
    list_of_image_dir = glob.glob("./plot_folder/*.png")
    last_name = None

    for j, i in enumerate(list_of_image_dir):
        list_of_ids = []
        name = re.findall(r"[A-Z\s]+", i)[0]

        if last_name != name:
            last_name = name
            list_of_dir = []
            for image_directories in list_of_image_dir:
                if last_name in image_directories:
                    list_of_dir.append(image_directories)

            pdf = FPDF()  # A4 (210 by 297 mm)

            ''' First Page '''
            pdf.add_page()
            create_title(day, pdf)
            create_logo(logo_dir, pdf)
            name = get_full_name(name)
            add_contact_info(name, pdf)

            internal_report = True

            if internal_report:
                legend_length = generate_legend(pdf, excel_directory)
                counter = 1
                minus_value = -(legend_length + 10)
                for image in tqdm(list_of_dir):
                    id = re.findall(r'[0-9]+', image)[0]
                    list_of_ids.append(id)
                    footer(pdf)
                    if counter == 3:
                        pdf.add_page()
                        minus_value = -25
                        counter = 0

                    pdf.image(image, 5, 80*counter-minus_value, WIDTH-20)
                    counter += 1
            else:
                counter = 0
                minus_value = -60
                for image in tqdm(list_of_dir):
                    footer(pdf)
                    if counter == 3:
                        pdf.add_page()
                        minus_value = -40
                        counter = 0
                    pdf.image(image, 5, 80*counter-minus_value, WIDTH-20)
                    counter += 1
            generate_raw_data_table(pdf, counter, list_of_ids)
            pdf.output("Report " + last_name + ".pdf", 'F')


if __name__ == '__main__':
    now = datetime.now()
    date = now.strftime("%d %B, %Y")
    create_analytics_report(date, excel_dir)

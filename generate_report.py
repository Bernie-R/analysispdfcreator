# Python libraries
from fpdf import FPDF
from datetime import datetime
import glob
import re
from tqdm import tqdm

# Local libraries
from generate_plots_lines import create_plot_acrylates, create_plot_photoinitiators

filename = "./output.pdf"

WIDTH = 210
HEIGHT = 297

logo_dir = "./resources/logo.jpg"

def create_title(day, pdf):
    # Unicode is not yet supported in the py3k version; use windows-1252 standard font
    pdf.set_font('Arial', '', 24)
    pdf.ln(10)
    pdf.write(5, f"Analytical Report")
    pdf.ln(10)
    pdf.set_font('Arial', '', 16)
    pdf.write(4, f'{day}')
    pdf.ln(5)

def create_logo(image_dir, pdf):
    pdf.ln(10)
    pdf.image(image_dir, 150, 8, 50)

def add_contact_info(name, pdf):
    pdf.set_font('Arial', '', 8)
    pdf.write(4, "Contact Information:")
    pdf.ln(3)
    pdf.write(4, "CENSORED")
    pdf.ln(3)
    pdf.write(4, "CENSORED")
    pdf.ln(5)
    pdf.write(4, f"Sample requester: {name}")


def create_analytics_report(day):
    now = datetime.now()
    date = now.strftime("%d %B, %Y")
    create_plot_photoinitiators(dir)
    list_of_image_dir = glob.glob("./plot_folder/*.png")
    last_name = None

    for j,i in enumerate(list_of_image_dir):
        sample_id = re.findall(r'\d+', i)[0]
        name = re.findall(r"[A-Z\s]+", i)[0]

        if last_name != name:
            last_name = name
            list_of_dir = []
            for l in list_of_image_dir:
                if last_name in l and "acrylate" in l:
                    list_of_dir.append(l)

            pdf = FPDF() # A4 (210 by 297 mm)

            ''' First Page '''
            pdf.add_page()
            #pdf.image("./resources/letterhead_cropped.png", 0, 0, WIDTH)
            create_title(day, pdf)
            create_logo(logo_dir, pdf)
            add_contact_info(name, pdf)

            counter = 1
            for image in tqdm(list_of_dir):
                    image_pic = image.replace("acrylate", "photoinitiator")
                    if counter % 4 == 0:
                        pdf.add_page()
                        counter = 1
                    pdf.image(image, 5, 80*(counter)-20, WIDTH/2-10)
                    pdf.image(image_pic, WIDTH/2, 80*(counter)-20, WIDTH/2-10)
                    counter += 1
            pdf.output("Report " + last_name + ".pdf", 'F')


if __name__ == '__main__':
    now = datetime.now()
    date = now.strftime("%d %B, %Y")
    create_analytics_report(date)

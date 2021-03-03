import pandas as pd


def read_excel_from_dir(excel_directory):
    data = pd.read_excel(excel_directory)
    return data


def read_a_and_p(df):
    # Material type
    acrylates_photoinitiators = {}
    for j, i in enumerate(df.iloc[0]):
        if " (ppb)" in i:
            i = i.replace(" (ppb)", "")
        acrylates_photoinitiators[j] = i
    acrylates_photoinitiators.pop(0, None)
    acrylates_photoinitiators.pop(1, None)
    return acrylates_photoinitiators


def read_sample_id(df):
    # sample_id
    sample_id = {}
    for j, i in enumerate(df.iloc[:, 0]):
        sample_id[i] = j + 2
    del sample_id["Sample"]
    del sample_id["CAS"]
    del sample_id["SML"]
    return sample_id


def read_sample_creator(df):
    # The sample creator
    sample_creator = {}
    for j, i in enumerate(df.iloc[:, 1]):
        if type(i) == str:
            sample_creator[j+2] = i
            save_name = i
        else:
            sample_creator[j+2] = save_name
    sample_creator.pop(2, None)
    sample_creator.pop(3, None)
    sample_creator.pop(4, None)
    return sample_creator


def read_cas(df):
    # Cas
    # Material Name
    cas = {}
    for j, i in enumerate(df.iloc[1]):
        if type(i) == str:
            cas[j] = i
        else:
            cas[j] = i
    cas.pop(0, None)
    cas.pop(1, None)
    return cas


def read_sml(df):
    # sml
    # Material Name
    sml = {}
    check = 0
    for j, i in enumerate(df.iloc[2]):
        if type(i) != int:
            sml[j] = check
        else:
            sml[j] = i
            check = i
    sml.pop(0, None)
    sml.pop(1, None)
    return sml


def read_which_are_acrylates_and_pi(data):
    # separate PI and ACR
    counter = 0
    a_p_dict = {}
    for i in data.head():
        if i == "Acrylates":
            a_p_dict[counter] = "Acrylates"
        if i == "Photoinitiators":
            a_p_dict[counter] = "Photoinitiators"
        counter += 1
    return a_p_dict

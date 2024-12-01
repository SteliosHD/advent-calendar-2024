import pandas as pd


def parser_raw_txt(file_path):
    with open(file_path) as file:
        return file.readlines()


def pandas_parser(file_path):
    return pd.read_csv(file_path, sep=r"\s+", header=None)

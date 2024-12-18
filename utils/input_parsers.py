import numpy as np
import pandas as pd

DUMMY_CONST = 91234


def parser_raw_txt(file_path):
    with open(file_path) as file:
        return file.readlines()


def parse_raw_txt_in_list(file_path: str, sep: str = " "):
    file_lines = parser_raw_txt(file_path)
    return [line.strip().split(sep) for line in file_lines]


def parse_raw_txt_string(file_path: str) -> str:
    with open(file_path) as file:
        return file.read().rstrip()


def pandas_parser(file_path, sep=r"\s+"):
    return pd.read_csv(file_path, sep=sep, header=None, on_bad_lines="warn")


def day_4_custom_parser(file_path, sep=r"\s+"):
    with open(file_path, "r") as file:
        lines = [line.strip().split(sep) for line in file]
    char_array_list = [[ch for ch in line[0]] for line in lines]
    return np.array(char_array_list).astype(str)


def pandas_custom_parser(file_path, sep=" ", dtype=int):
    with open(file_path, "r") as file:
        lines = [line.strip().split(sep) for line in file]
    max_columns = max(len(line) for line in lines)

    padded_lines = [line + [DUMMY_CONST] * (max_columns - len(line)) for line in lines]
    return pd.DataFrame(padded_lines).map(
        lambda x: int(x) if x is not None and pd.notna(x) else x
    )

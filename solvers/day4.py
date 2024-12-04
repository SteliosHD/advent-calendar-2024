from functools import lru_cache
from typing import Optional

import numpy as np

from solvers.base_solver import BaseSolver
from utils.input_parsers import day_4_custom_parser


class Array2DReader:
    def __init__(self, array: np.array):
        self.array: np.ndarray = array
        self.mask_array = np.zeros(self.array.shape)

    def read(
        self,
        pos: (int, int),
        direction: (int, int),
        include_pos: bool = True,
        override_array: Optional[np.ndarray] = None,
        max_read: int = 4,
    ) -> tuple[list[str] | list, tuple[list[int] | list, list[int] | list]]:
        """
        Generalized method to read in a given direction.

        Args:
            pos (int, int): Starting position (row, column).
            direction (int, int): Direction vector (row_step, col_step).
            include_pos (bool): Whether to include the starting position.
            override_array (np.array): Optional override for the array to read.
            max_read (int) : How many characters to read

        Returns:
            list[str]: Elements read in the specified direction.
        """
        array_to_read = self.array if override_array is None else override_array
        rows, cols = array_to_read.shape
        read_arr = [str(array_to_read[pos])] if include_pos else []
        curr_row, curr_col = pos

        row_span = [int(curr_row)] if include_pos else []
        col_span = [int(curr_col)] if include_pos else []

        while len(read_arr) < max_read:
            curr_row += direction[0]
            curr_col += direction[1]
            row_span.append(curr_row)
            col_span.append(curr_col)
            if not (0 <= curr_row < rows and 0 <= curr_col < cols):
                col_span.pop(), row_span.pop()
                break
            read_arr.append(str(array_to_read[curr_row][curr_col]))

        return read_arr, (row_span, col_span)

    def read_left(self, pos, **kwargs):
        return self.read(pos, direction=(0, -1), **kwargs)

    def read_right(self, pos, **kwargs):
        return self.read(pos, direction=(0, 1), **kwargs)

    def read_up(self, pos, **kwargs):
        return self.read(pos, direction=(-1, 0), **kwargs)

    def read_down(self, pos, **kwargs):
        return self.read(pos, direction=(1, 0), **kwargs)

    def read_diag_up_right(self, pos, **kwargs):
        return self.read(pos, direction=(-1, 1), **kwargs)

    def read_diag_up_left(self, pos, **kwargs):
        return self.read(pos, direction=(-1, -1), **kwargs)

    def read_diag_down_right(self, pos, **kwargs):
        return self.read(pos, direction=(1, 1), **kwargs)

    def read_diag_down_left(self, pos, **kwargs):
        return self.read(pos, direction=(1, -1), **kwargs)

    def get_mask_array(self):
        return self.mask_array

    def update_mask_array(self, row_span: list[int], col_span: list[int]):
        for i, j in zip(row_span, col_span):
            self.mask_array[i][j] = 1

    def bulk_update_mask_array(
        self, update_positions: list[tuple[list[int], list[int]]]
    ):
        for position in update_positions:
            self.update_mask_array(*position)

    @staticmethod
    def extract_matching_word_positions(
        position_dict: dict[
            str, tuple[list[str] | list, tuple[list[int] | list, list[int] | list]]
        ],
        match_pattern="XMAS",
    ) -> list[tuple[list[int], list[int]]]:
        positions = []
        for values in position_dict.values():
            if "".join(values[0]).upper() == match_pattern.upper():
                positions.append(values[1])
        return [
            (list(a), list(b))
            for a, b in {tuple(map(tuple, pair)) for pair in positions}
        ]

    def read_all(
        self, pos, **kwargs
    ) -> dict[str, tuple[list[str] | list, tuple[list[int] | list, list[int] | list]]]:
        return {
            "up": self.read_up(pos, **kwargs),
            "down": self.read_down(pos, **kwargs),
            "left": self.read_left(pos, **kwargs),
            "right": self.read_right(pos, **kwargs),
            "diag_up_right": self.read_diag_up_right(pos, **kwargs),
            "diag_up_left": self.read_diag_up_left(pos, **kwargs),
            "diag_down_right": self.read_diag_down_right(pos, **kwargs),
            "diag_down_left": self.read_diag_down_left(pos, **kwargs),
        }

    def is_x_pattern(
        self,
        pos: (int, int),
        override_array: Optional[np.ndarray] = None,
        x_patterns=(
            (
                ("M", "*", "M"),
                ("*", "A", "*"),
                ("S", "*", "S"),
            ),
            (
                ("M", "*", "S"),
                ("*", "A", "*"),
                ("M", "*", "S"),
            ),
            (
                ("S", "*", "M"),
                ("*", "A", "*"),
                ("S", "*", "M"),
            ),
            (
                ("S", "*", "S"),
                ("*", "A", "*"),
                ("M", "*", "M"),
            ),
        ),
    ) -> tuple[bool, Optional[tuple[list[int], list[int]]]]:
        array_to_read = self.array if override_array is None else override_array
        rows, cols = array_to_read.shape
        curr_row, curr_col = pos
        if (
            curr_row == 0
            or curr_row == rows - 1
            or curr_col == 0
            or curr_col == cols - 1
        ):
            return False, None
        window = (
            (
                str(array_to_read[curr_row - 1][curr_col - 1]),
                "*",
                str(array_to_read[curr_row - 1][curr_col + 1]),
            ),
            (
                "*",
                str(array_to_read[curr_row][curr_col]),
                "*",
            ),
            (
                str(array_to_read[curr_row + 1][curr_col - 1]),
                "*",
                str(array_to_read[curr_row + 1][curr_col + 1]),
            ),
        )
        if window in x_patterns:
            return (
                True,
                (
                    [curr_row - 1, curr_row - 1, curr_row, curr_row + 1, curr_row + 1],
                    [curr_col - 1, curr_col + 1, curr_col, curr_col - 1, curr_col + 1],
                ),
            )
        return False, None


class Day4Solver(BaseSolver):
    @lru_cache
    def _parse_input(self):
        return day_4_custom_parser(self.input_path)

    def _part_one(self, debug=False) -> any:
        input_array = self._parse_input()
        array_reader = Array2DReader(input_array)
        occurrences = 0
        for i, j in np.ndindex(input_array.shape):
            read_positions = array_reader.read_all((i, j))
            xmas_positions = array_reader.extract_matching_word_positions(
                read_positions
            )
            occurrences += len(xmas_positions)
            array_reader.bulk_update_mask_array(xmas_positions)
        if debug:
            print(array_reader.get_mask_array())
        return occurrences

    def _part_two(self, debug=False) -> any:
        input_array = self._parse_input()
        array_reader = Array2DReader(input_array)
        for i, j in np.ndindex(input_array.shape):
            read_positions = array_reader.read_all((i, j), max_read=3)
            xmas_positions = array_reader.extract_matching_word_positions(
                read_positions, match_pattern="MAS"
            )
            array_reader.bulk_update_mask_array(xmas_positions)
        mas_input_array = np.where(array_reader.get_mask_array() == 0, ".", input_array)
        mas_array_reader = Array2DReader(mas_input_array)
        occurrences = 0
        for i, j in np.ndindex(mas_input_array.shape):
            is_x_mas, position_array = mas_array_reader.is_x_pattern((i, j))
            if is_x_mas:
                mas_array_reader.update_mask_array(*position_array)
                occurrences += 1
        if debug:
            print(mas_array_reader.get_mask_array())
        return occurrences


day4 = Day4Solver("day 4", "inputs/day4.csv")

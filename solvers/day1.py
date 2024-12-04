from functools import lru_cache

from solvers.base_solver import BaseSolver
from utils.input_parser import pandas_parser
import numpy.typing as npt
import collections


class Day1Solver(BaseSolver):
    @lru_cache
    def _parse_input(self):
        input_df = pandas_parser(self.input_path)
        left_column: npt.NDArray = input_df[0].to_numpy()
        right_column: npt.NDArray = input_df[1].to_numpy()
        return left_column, right_column

    def _part_one(self, debug=False) -> int:
        left_column, right_column = self._parse_input()
        left_column.sort()
        right_column.sort()
        return sum(abs(left_column - right_column))

    def _part_two(self, debug=False) -> int:
        left_column, right_column = self._parse_input()
        left_column.sort()
        right_column.sort()
        counter = collections.Counter(right_column)
        similarity_index = 0
        for value in left_column:
            sim_index = counter.get(value, 0) * value
            similarity_index += sim_index
        return similarity_index


day1 = Day1Solver("day 1", "inputs/day1.csv")

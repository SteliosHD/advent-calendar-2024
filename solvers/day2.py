from functools import lru_cache

import numpy as np
import numpy.typing as npt

from solvers.base_solver import BaseSolver
from utils.input_parser import pandas_custom_parser, DUMMY_CONST


class Day2Solver(BaseSolver):
    @lru_cache
    def _parse_input(self):
        input_df = pandas_custom_parser(self.input_path, sep=" ")
        return input_df

    def _part_one(self, debug=False) -> int:
        input_df = self._parse_input()
        count_safe = 0
        np_array = input_df.to_numpy(dtype=int)
        for line in np_array:
            if is_safe := self._is_line_ordered(line):
                if debug:
                    print(f"line {line} is safe: {is_safe}")
                count_safe += 1
        return count_safe

    def _part_two(self, debug=False) -> int:
        input_df = self._parse_input()
        count_safe = 0
        np_array = input_df.to_numpy(dtype=int)
        for line in np_array:
            for comb_line in self._get_combinations(line):
                if is_safe := self._is_line_ordered(comb_line):
                    if debug:
                        print(f"line {comb_line} is safe: {is_safe}")
                    count_safe += 1
                    break
        return count_safe

    @staticmethod
    def _get_combinations(line: np.array(int)):
        return [np.delete(line, i) for i in range(len(line))]

    @staticmethod
    def _is_line_ordered(line: npt.NDArray):
        if len(line) < 2:
            return True
        ascending = True
        descending = True
        strict_ascending = True
        strict_descending = True

        for i in range(len(line) - 1):
            if line[i + 1] == DUMMY_CONST:
                return True
            diff = line[i + 1] - line[i]
            if ascending and diff <= 0:
                ascending = False
                strict_ascending = False
            if descending and diff >= 0:
                descending = False
                strict_descending = False
            if diff > 3 and ascending:
                ascending = False
            if diff < -3 and descending:
                descending = False
            if diff == 0:
                ascending = descending = False
            if not ascending and not descending:
                return False
            if not strict_ascending and not strict_descending:
                return False
        return ascending or descending

    @lru_cache()
    def _level_diff(self, start_level: int, end_level: int):
        return end_level - start_level


day2 = Day2Solver("day 2", "inputs/day2.csv")


def test_test_case():
    solv = Day2Solver("day 2 test", "../inputs/day2test.csv")
    test_df = solv._parse_input()
    count_safe = 0
    np_array = test_df.to_numpy(dtype=int)
    safe_indexes = set()
    for index, line in enumerate(np_array):
        for comb_line in solv._get_combinations(line):
            if is_safe := solv._is_line_ordered(comb_line):
                print(f"\nline {comb_line} is safe: {is_safe}")
                safe_indexes.add(index)
                count_safe += 1
                break
    assert count_safe == 4
    assert safe_indexes == {0, 3, 4, 5}

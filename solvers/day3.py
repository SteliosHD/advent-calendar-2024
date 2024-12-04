import re
from functools import lru_cache


from solvers.base_solver import BaseSolver
from utils.input_parsers import parse_raw_txt_string


class Day3Solver(BaseSolver):
    @lru_cache
    def _parse_input(self):
        return parse_raw_txt_string(self.input_path)

    def _part_one(self, debug=False) -> int:
        text = self._parse_input()
        regex_pattern = r"mul\(\d+,\d+\)"
        all_occurrences = re.findall(regex_pattern, text)
        return self._calculate_sum(all_occurrences)

    @staticmethod
    def _extract_numbers(occurrence: str) -> list[int]:
        return [int(x) for x in re.findall(r"\d+", occurrence)]

    def _calculate_sum(self, all_occurrences: list[str]) -> int:
        product_sum = 0
        for occur in all_occurrences:
            numbers = self._extract_numbers(occur)
            product_sum += numbers[0] * numbers[1]
        return product_sum

    def _calculate_sum_controlled(self, tokens: list):
        enabled = True
        product_sum = 0

        for token in tokens:
            if token == "do()":
                enabled = True
            elif token == "don't()":
                enabled = False
            elif enabled and token:
                numbers = self._extract_numbers(token)
                product_sum += numbers[0] * numbers[1]
        return product_sum

    def _part_two(self, debug=False) -> int:
        input_memory_string = self._parse_input()
        mul_pattern = r"mul\(\d+,\d+\)"
        control_pattern = r"do\(\)|don't\(\)"
        tokens = re.findall(f"{mul_pattern}|{control_pattern}", input_memory_string)
        return self._calculate_sum_controlled(tokens)


day3 = Day3Solver("day 3", "inputs/day3.csv")

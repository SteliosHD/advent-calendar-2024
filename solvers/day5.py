from functools import lru_cache

from solvers.base_solver import BaseSolver
from utils.input_parsers import parse_raw_txt_in_list


class Day5Solver(BaseSolver):
    @lru_cache
    def _parse_input(self) -> tuple[list[str], tuple[tuple[int, ...], ...]]:
        constraints = parse_raw_txt_in_list(self.input_paths[0])
        pages_to_produce = parse_raw_txt_in_list(self.input_paths[1])
        return [c[0] for c in constraints], tuple(
            tuple([int(elem) for elem in page[0].split(",")])
            for page in pages_to_produce
        )

    def _part_one(self, debug=False) -> tuple[int, list]:
        constraints, pages_to_produce = self._parse_input()
        page_ordering_rules = self._generate_page_ordering_rules(constraints)
        correct_ordered_updates = []
        bad_ordered_updates = []
        for line in pages_to_produce:
            valid_update = True
            for index, page in enumerate(line):
                order_rule = page_ordering_rules.get(page)
                if self._rule_is_violated(order_rule, line[:index]):
                    valid_update = False
                    bad_ordered_updates.append(line)
                    break
            if valid_update:
                correct_ordered_updates.append(line)
        return sum(
            [line[int((len(line) - 1) / 2)] for line in correct_ordered_updates]
        ), bad_ordered_updates

    @staticmethod
    @lru_cache
    def _rule_is_violated(order_rule: tuple[int, ...], line: tuple[int, ...]) -> bool:
        return len(set(order_rule).intersection(set(line))) != 0

    @staticmethod
    def _generate_page_ordering_rules(
        constraints: list[str],
    ) -> dict[int, tuple[int, ...]]:
        page_ordering_rules: dict[int, list[int]] = {}
        for line in constraints:
            page_number, must_be_before_page = line.split("|")
            page_ordering_rules.setdefault(int(page_number), []).append(
                int(must_be_before_page)
            )
        return {int(key): tuple(val) for key, val in page_ordering_rules.items()}

    def _part_two(self, debug=False) -> any:
        _, bad_updates = self._part_one()
        return bad_updates


day5 = Day5Solver(
    "day 5", input_paths=["inputs/day5Constraints.csv", "inputs/day5Instructions.csv"]
)

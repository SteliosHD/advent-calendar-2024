from abc import ABC


class BaseSolver(ABC):
    def __init__(self, day: str, input_path: str):
        self.day: str = day
        self.input_path: str = input_path

    def run(self, part: int = 1, print_result=True):
        if part == 1:
            result = self._part_one()
        elif part == 2:
            result = self._part_two()
        else:
            raise ValueError("Part must be 1 or 2")
        if not print_result:
            return result
        print(result)

    def _part_one(self) -> any:
        pass

    def _part_two(self) -> any:
        pass

    def _parse_input(self):
        pass

    def print_raw_input(self):
        with open(self.input_path) as file:
            print(file.readlines())

    def __str__(self):
        return f"Solver for {self.day}, Input path: {self.input_path}"
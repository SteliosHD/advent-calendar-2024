from abc import ABC


class BaseSolver(ABC):
    def __init__(self, day: str, input_path: str = "", input_paths=None):
        self.day: str = day
        self.input_path: str = input_path
        self.input_paths: list[str] = input_paths

    def run(self, part: int = 1, print_result=True, debug=False):
        if part == 1:
            result = self._part_one(debug)
        elif part == 2:
            result = self._part_two(debug)
        else:
            raise ValueError("Part must be 1 or 2")
        if not print_result:
            return result
        print(result)

    def _part_one(self, debug=False) -> any:
        raise NotImplementedError("Part one is not implemented yet")

    def _part_two(self, debug=False) -> any:
        raise NotImplementedError("Part two is not implemented yet")

    def _parse_input(self) -> any:
        pass

    def print_raw_input(self):
        with open(self.input_path) as file:
            print(file.read())

    def __str__(self):
        return f"Solver for {self.day}, Input path: {self.input_path}"

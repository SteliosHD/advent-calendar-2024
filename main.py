import typer
from importlib import import_module

app = typer.Typer()

day_solvers_modules_instances = {
    1: ["solvers.day1", "day1"],
    2: ["solvers.day2", "day2"],
    3: ["solvers.day3", "day3"],
    4: ["solvers.day4", "day4"],
}


def create_command(day: int, part: int, instance_name: str):
    """
    Factory function to create a command for a specific day and part.
    """

    def command(debug: bool = typer.Option(False, "--debug", help="Enable debug mode")):
        solver_module = import_module(
            day_solvers_modules_instances[day][0],
        )
        solver_instance = getattr(solver_module, instance_name)
        solver_instance.run(part=part, debug=debug)

    return command


for day, module_instance in day_solvers_modules_instances.items():
    for part in [1, 2]:
        command_name = f"{day}{'A' if part == 1 else 'B'}"
        app.command(name=command_name)(create_command(day, part, module_instance[1]))

if __name__ == "__main__":
    app()

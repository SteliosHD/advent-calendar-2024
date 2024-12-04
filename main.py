import typer

from solvers.day2 import day2
from solvers.day1 import day1

app = typer.Typer()


@app.command(name="1A")
def day_1_first():
    day1.run(part=1)


@app.command(name="1B")
def day_1_second():
    day1.run(part=2)


@app.command(name="2A")
def day_2_first(debug: bool = typer.Option(False, "--debug", help="Enable debug mode")):
    day2.run(part=1, debug=debug)


@app.command(name="2B")
def day_2_second(
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    day2.run(part=2, debug=debug)


if __name__ == "__main__":
    app()

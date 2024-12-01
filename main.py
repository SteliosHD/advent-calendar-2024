import typer
from solvers.day1 import day1

app = typer.Typer()


@app.command(name="1A")
def day_1_first():
    day1.run(part=1)


@app.command(name="1B")
def day_1_second():
    day1.run(part=2)


if __name__ == "__main__":
    app()

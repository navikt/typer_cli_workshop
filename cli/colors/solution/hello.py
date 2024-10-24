import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()
console = Console()


def create_table() -> Table:
    """Hjelpemetode for å generere en tabell i `rich`"""
    table = Table(title="Star Wars Movies")

    table.add_column("Released", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Box Office", justify="right", style="green")

    table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
    table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
    table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
    table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

    return table


@app.command()
def main(name: str, formal: bool = False, summary: bool = False) -> None:
    """Si hei til det gitte navnet"""
    if formal:
        console.print(f"Hallo {name} :top_hat:")
    else:
        console.print(f"Hei [bold magenta]{name}[/]!")
    if summary:
        console.print(create_table())


if __name__ == "__main__":
    app()

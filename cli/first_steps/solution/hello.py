import typer

app = typer.Typer()


@app.command()
def main(name: str, formal: bool = False) -> None:
    """Si hei til det gitte navnet"""
    if formal:
        print(f"Hallo {name}")
    else:
        print(f"Hei {name}!")


if __name__ == "__main__":
    app()

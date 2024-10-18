import pathlib
import time
from typing import Annotated, Any

import httpx
import typer
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

app = typer.Typer()
console = Console()


def create_summary(summary_data: dict[str, Any]) -> Table:
    """Hjelpemetode for å lage en `rich` tabell"""
    table = Table(title="Oppsummering")

    table.add_column("Nettside", style="bold magenta")
    table.add_column("Antall bytes", style="italic")
    table.add_column("Lagringssted", justify="right")

    for webpage in summary_data:
        data = summary_data[webpage]
        table.add_row(webpage, data["bytes"], data["path"])
    
    return table


@app.command()
def main(
    webpages: list[str],
    folder: pathlib.Path | None = None,
    summary: Annotated[bool, typer.Option("--show-summary")] = False,
) -> None:
    if folder:
        if folder.exists() and not folder.is_dir():
            console.print(f"[bold red]Kan ikke laste ned til [i]{folder}[/i], det er ikke en mappe!")
            raise typer.Abort()
        elif not folder.exists():
            folder.mkdir()
    summary_data = {}
    with Progress(console=console) as progress:
        task = progress.add_task("Nettsider lastet ned", total=len(webpages))
        for webpage in webpages:
            page_response = httpx.get("https://" + webpage)
            if page_response.status_code != 200:
                console.print(f"[red] Klarte ikke å laste ned [bold]{webpage}[/bold]!")
            else:
                size: int = page_response.headers.get("Content-Length", len(page_response.content))
                page_task = progress.add_task(f"Laster ned [italic magenta]{webpage}[/]", total=size)
                file_path = webpage if not folder else folder / webpage
                with open(file_path, mode="wb") as fil:
                    for chunk in page_response.iter_bytes(512):
                        wrote = fil.write(chunk)
                        progress.advance(page_task, advance=wrote)
                        time.sleep(0.0005)
                progress.remove_task(page_task)
                summary_data[webpage] = {"bytes": str(size), "path": str(file_path)}
            progress.advance(task, advance=1)
    if summary and summary_data:
        console.print(create_summary(summary_data))


if __name__ == "__main__":
    app()

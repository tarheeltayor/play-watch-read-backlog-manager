"""Main CLI."""

from pathlib import Path
from typing import Annotated

import typer

from .book.cli import book_app
from .game.cli import game_app
from .manager import BacklogManager

app = typer.Typer(no_args_is_help=True)


@app.callback()
def main_callback(
    ctx: typer.Context,
    backlog: Annotated[Path, typer.Option(help="Where to find backlog file.")] = Path("backlog.json"),
) -> None:
    """Provide global flag for CLI."""
    ctx.obj = BacklogManager.from_file(backlog)


app.add_typer(game_app, name="game", no_args_is_help=True)
app.add_typer(book_app, name="book", no_args_is_help=True)


if __name__ == "__main__":
    app()

import typer

from .sideroxylon import sideroxylon


app = typer.Typer()
app.command()(sideroxylon)


if __name__ == "__main__":
    app()

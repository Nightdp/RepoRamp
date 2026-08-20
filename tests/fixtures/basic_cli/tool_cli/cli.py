import typer

app = typer.Typer()


@app.command()
def main() -> None:
    print("hello")


if __name__ == "__main__":
    app()

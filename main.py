import typer
from sudo_sql.pipeline import UnifiedPipeline

app = typer.Typer()

@app.command()
def train(config: str = typer.Option(..., "--config", help="Path to the training configuration file.")):
    """Train a model."""
    pipeline = UnifiedPipeline(config_path=config)
    pipeline.run()

@app.command()
def infer(config: str = typer.Option(..., "--config", help="Path to the inference configuration file.")):
    """Run inference with a model."""
    pipeline = UnifiedPipeline(config_path=config)
    pipeline.run()

if __name__ == "__main__":
    app()
from pathlib import Path
from pipeline.hand_pipeline import run_pipeline


def main():
    print("Iniciando pipeline HAND...")

    outdir = Path("outputs_dem")

    run_pipeline(outdir)

    print("Concluído.")


if __name__ == "__main__":
    main()
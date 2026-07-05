import subprocess
import sys
from pathlib import Path


def main() -> None:
    raw_root = Path("data/raw")

    if not raw_root.exists():
        print("data/raw does not exist.")
        sys.exit(1)

    state_folders = sorted(
        folder for folder in raw_root.iterdir() if folder.is_dir()
    )

    if not state_folders:
        print("No state folders found.")
        return

    for folder in state_folders:
        state_code = folder.name.upper()

        json_files = list(folder.glob("*.json"))

        if not json_files:
            print(f"{state_code}: No JSON files found. Skipping.")
            continue

        print()
        print("=" * 50)
        print(f"Exporting {state_code}")
        print("=" * 50)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "src.unclaimed_property.cli.export_state",
                state_code,
                str(folder),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
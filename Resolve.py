import sys
import subprocess
from pathlib import Path

def hash(file: Path) -> str:
    return subprocess.check_output(f"git hash-object {file}", text=True, shell=True).rstrip()

def main(argv):
    if len(argv) != 4:
        print(f"""Usage: {argv[0]} <start-scheme> <stop-scheme> <transformations-dir>

        If the database scheme is newer than the CodeQL pack scheme then we need to downgrade the database.
        In this case the <start-scheme> is the database scheme, the <stop-scheme> is the CodeQL pack scheme
        and the <transformation-dir> is the downgrades folder of the language extractor $(codeql resolve extractor --language=cpp)

        If the CodeQL pack scheme is newer the scheme should be swapped and the <transformation-dir> should point to the
        upgrades folder part of the CodeQL pack.
        """)
        sys.exit(1)

    start_schema = Path(argv[1])
    stop_schema = Path(argv[2])
    transformations_dir = Path(argv[3])

    start_schema_hash = hash(start_schema)
    stop_schema_hash = hash(stop_schema)

    next_hash = start_schema_hash
    while next_hash != stop_schema_hash:
        print(f"Looking to transform {next_hash}")
        next_schema_path = transformations_dir / next_hash / start_schema.name
        if not next_schema_path.exists():
            print("Failed to find transformation path from {start_schema} to {stop_schema}, got stuck at {next_schema}")
        
        current_hash = next_hash
        next_hash = hash(next_schema_path)
        print(f"Transformed {current_hash} to {next_hash}")
    
    print(f"Done, transformed {start_schema}({start_schema_hash}) to {stop_schema}({stop_schema_hash})")
    

if __name__ == "__main__":
    main(sys.argv)
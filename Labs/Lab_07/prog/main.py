from part1_linq_to_objects import run as run_objects
from part2_linq_to_json import run as run_json
from part3_linq_to_sql import run as run_sql

if __name__ == "__main__":
    print("\n=== LINQ to Objects ===")
    run_objects()

    print("\n=== LINQ to JSON ===")
    run_json()

    print("\n=== LINQ to SQL ===")
    run_sql()


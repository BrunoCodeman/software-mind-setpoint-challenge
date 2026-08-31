import csv
from pathlib import Path

from movie_analyzer import Movie, refactor_movie_list, top_certified_fresh_movies


TRUE_VALUES = {"true", "1", "yes"}
FALSE_VALUES = {"false", "0", "no"}


def analyze_csv(file_path: str | Path) -> list[Movie]:
    """Read movies from a CSV, print the top certified-fresh results, and return them."""
    with Path(file_path).open(newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [
            [
                row["id"],
                row["rating"],
                row["movie_title"],
                _parse_bool(row["certified_fresh"]),
            ]
            for row in reader
        ]

    top_movies = top_certified_fresh_movies(refactor_movie_list(rows))
    print("Top certified-fresh movies")
    for rank, movie in enumerate(top_movies, start=1):
        print(f"{rank:>2}. {movie.movie_title} ({movie.rating:.1f}/10.0)")
    return top_movies


def _parse_bool(value: str) -> bool:
    normalized_value = value.strip().lower()
    if normalized_value in TRUE_VALUES:
        return True
    if normalized_value in FALSE_VALUES:
        return False
    raise ValueError(f"Invalid certified_fresh value: {value!r}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print the top certified-fresh movies.")
    parser.add_argument("file_path", type=Path)
    analyze_csv(parser.parse_args().file_path)

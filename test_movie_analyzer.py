import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from main import analyze_csv
from movie_analyzer import Movie, refactor_movie_list, top_certified_fresh_movies


class MovieAnalyzerTests(unittest.TestCase):
    def test_refactor_movie_list_creates_movie_records(self):
        movies = refactor_movie_list([[1, 9.0, "Jurassic Park", True]])

        self.assertEqual(
            movies,
            [Movie(1, 9.0, "Jurassic Park", True)],
        )

    def test_top_certified_fresh_movies_filters_and_sorts(self):
        movie_list = [
            [1, 9.0, "Interstellar", True],
            [2, 10.0, "Avatar", False],
            [3, 9.5, "Arrival", True],
        ]

        result = top_certified_fresh_movies(movie_list)

        self.assertEqual(
            [movie.movie_title for movie in result],
            ["Arrival", "Interstellar"],
        )

    def test_top_certified_fresh_movies_returns_at_most_ten(self):
        movie_list = [
            [index, float(index), f"Movie {index}", True]
            for index in range(1, 13)
        ]

        result = top_certified_fresh_movies(movie_list)

        self.assertEqual(len(result), 10)
        self.assertEqual(result[0].rating, 12.0)
        self.assertEqual(result[-1].rating, 3.0)

    def test_analyze_csv_reads_prints_and_returns_top_movies(self):
        csv_content = (
            "id,rating,movie_title,certified_fresh\n"
            "1,9.0,Interstellar,true\n"
            "2,8.5,Fast and the Furious,false\n"
            "3,9.5,Arrival,yes\n"
        )
        output = io.StringIO()

        with tempfile.TemporaryDirectory() as directory:
            file_path = Path(directory) / "movies.csv"
            file_path.write_text(csv_content, encoding="utf-8")
            with redirect_stdout(output):
                result = analyze_csv(file_path)

        self.assertEqual([movie.movie_title for movie in result], ["Arrival", "Interstellar"])
        self.assertEqual(
            output.getvalue(),
            "Top certified-fresh movies\n"
            " 1. Arrival (9.5/10.0)\n"
            " 2. Interstellar (9.0/10.0)\n",
        )


if __name__ == "__main__":
    unittest.main()

from dataclasses import dataclass
from typing import Iterable, Sequence


@dataclass(frozen=True)
class Movie:
    id: int
    rating: float
    movie_title: str
    certified_fresh: bool


MovieRow = Sequence[int | float | str | bool]


def refactor_movie_list(movie_list: Iterable[MovieRow]) -> list[Movie]:
    """Convert positional CSV rows into readable Movie records."""
    return [
        Movie(
            id=int(row[0]),
            rating=float(row[1]),
            movie_title=str(row[2]),
            certified_fresh=bool(row[3]),
        )
        for row in movie_list
    ]


def top_certified_fresh_movies(movie_list: Iterable[Movie | MovieRow]) -> list[Movie]:
    """Return the ten highest-rated certified-fresh movies."""
    movies = [
        movie if isinstance(movie, Movie) else refactor_movie_list([movie])[0]
        for movie in movie_list
    ]
    return sorted(
        (movie for movie in movies if movie.certified_fresh),
        key=lambda movie: movie.rating,
        reverse=True,
    )[:10]

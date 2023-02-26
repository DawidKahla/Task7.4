from random import choice, randint
from datetime import date


class Movie:
    def __init__(self, title, publication_year, genre, views):
        self.title = title
        self.publication_year = publication_year
        self.genre = genre
        self.views = views

    def play(self):
        self.views += 1

    def __repr__(self):
        return f"{self.title} ({self.publication_year})"


class Series(Movie):
    def __init__(self, episode_number, season_number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.episode_number = episode_number
        self.season_number = season_number

    def __repr__(self):
        return f"{self.title} S{self.season_number:02d}E{self.episode_number:02d}"


def get_production(production_list, content_type):
    output_list = []
    for production in production_list:
        if type(production) == content_type:
            output_list.append(production)
    return sorted(output_list, key=lambda x: x.title.lower())


# return list of movies from production_list sorted alphabeticaly doesnt support foreign characters
def get_movies(production_list):
    return get_production(production_list, Movie)


# return list of series from production_list sorted alphabeticaly doesnt support foreign characters
def get_series(production_list):
    return get_production(production_list, Series)


# returns list of specified productions
def search(title, production_list):
    list_of_productions = []
    for production in production_list:
        if title == production.title:
            list_of_productions.append(production)
    return list_of_productions


# adding random number from 1 to 100 to random production from production_list
def generate_views(production_list):
    choice(production_list).views += randint(1, 100)


def generate_views10times(production_list):
    for i in range(10):
        generate_views(production_list)


# returns list of most viewed productions/series/movies depend on content_type arg
def top_titles(production_list, content_type, number_top):
    if content_type == Movie:
        production_list = get_movies(production_list)
    elif content_type == Series:
        production_list = get_series(production_list)
    content_type_sorted_by_views_list = sorted(
        production_list, key=lambda x: x.views, reverse=True
    )
    specified_number_of_most_viewed_content_type_list = (
        content_type_sorted_by_views_list[:number_top]
    )
    return specified_number_of_most_viewed_content_type_list


# adding whole season of specified series | if episodes went on different years it have to be used multiple times
def add_series_season(
    production_list, title, publication_year, genre, season_number, episodes_number
):
    for episode_number in range(1, episodes_number + 1):
        production_list.append(
            Series(
                title=title,
                publication_year=publication_year,
                views=0,
                genre=genre,
                season_number=season_number,
                episode_number=episode_number,
            )
        )
    return production_list


# prints number of episodes of specified series and season in production_list
def print_number_of_episodes(production_list, title, season):
    output_number = 0
    series_list = get_series(production_list)
    series_list = search(title, series_list)
    for serie in series_list:
        if serie.season_number == season:
            output_number += 1
    print(
        f"Serial: {title}, Sezon: {season}, Ilość odcinków w bibliotece: {output_number}"
    )


if __name__ == "__main__":
    print("Biblioteka filmów")

    library = []
    library.append(
        Movie(title="Poranek kojota", publication_year="2001", genre="Komedia", views=0)
    )
    library.append(
        Movie(
            title="Chłopaki nie płaczą",
            publication_year="2000",
            genre="Komedia",
            views=0,
        )
    )
    library.append(
        Series(
            title="Moda na sukces",
            publication_year="1987",
            genre="Opera mydlana",
            views=0,
            season_number=35,
            episode_number=8947,
        )
    )
    library.append(
        Series(
            title="Gra o tron",
            publication_year="2011",
            genre="Fantasy",
            views=0,
            season_number=8,
            episode_number=73,
        )
    )
    library.append(
        Movie(
            title="Skazani na Shawshank",
            publication_year="1994",
            genre="Film fabularny",
            views=0,
        )
    )
    library = add_series_season(
        production_list=library,
        title="Zmiennicy",
        publication_year=1987,
        genre="Komedia",
        season_number=1,
        episodes_number=15,
    )

    generate_views10times(library)
    generate_views10times(library)
    generate_views10times(library)

    today = date.today()
    today = today.strftime("%d.%m.%Y")
    print(f"Najpopularniejsze filmy i seriale dnia {today}")
    print(top_titles(library, "", 3))

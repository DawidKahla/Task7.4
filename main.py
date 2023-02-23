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
        # Czy da się lepiej/prościej rozwiązać wymuszenie dwucyfrowej notacji?
        ep_number = self.episode_number
        s_number = self.season_number
        if ep_number < 10:
            ep_number = "0" + str(ep_number)
        if s_number < 10:
            s_number = "0" + str(s_number)
        return f"{self.title} S{s_number}E{ep_number}"


# return list of movies from production_list sorted alphabeticaly doesnt support foreign characters
def get_movies(production_list):
    output_list = []
    for production in production_list:
        if isinstance(production, Movie) and not isinstance(production, Series):
            output_list.append(production)
    output_list = sorted(output_list, key=lambda x: x.title.lower())
    return output_list


# return list of series from production_list sorted alphabeticaly doesnt support foreign characters
def get_series(production_list):
    output_list = []
    for production in production_list:
        if isinstance(production, Series):
            output_list.append(production)
    output_list = sorted(output_list, key=lambda x: x.title.lower())
    return output_list


# returns specific production from production_list or list of them if there is multiple or blank list if there is not
def search(title, production_list):
    flag = 0
    list_of_productions = []
    for production in production_list:
        if title == production.title:
            flag += 1
            output_production = production
            list_of_productions.append(production)
    if flag == 0:
        print("Nie znaleziono zadanego tytułu.")
        return []
    if flag > 1:
        return list_of_productions
    return output_production


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
    if content_type == Series:
        production_list = get_series(production_list)
    top_list = sorted(production_list, key=lambda x: x.views, reverse=True)
    top_list = top_list[: -(len(top_list) - number_top)]
    return top_list


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


print("Biblioteka filmów")

library = []
library.append(
    Movie(title="Poranek kojota", publication_year="2001", genre="Komedia", views=0)
)
library.append(
    Movie(
        title="Chłopaki nie płaczą", publication_year="2000", genre="Komedia", views=0
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

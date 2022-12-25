from flask import Flask

from utils import film_research_by_title, film_research_by_years, film_research_by_rating, film_research_by_genre

app = Flask(__name__)


@app.route('/movie/<title>')
def search_by_title(title):
    return film_research_by_title(title)


@app.route('/movie/<int:year1>/to/<int:year2>')
def search_by_year(year1, year2):
    return film_research_by_years(year1, year2)


@app.route('/rating/<rating>')
def search_by_rating(rating):
    return film_research_by_rating(rating)


@app.route('/genre/<genre>')
def search_by_genre(genre):
    return film_research_by_genre(genre)


if __name__ == '__main__':
    app.run()

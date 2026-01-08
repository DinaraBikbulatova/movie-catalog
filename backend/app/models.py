import json
import os


class FilmManager:
    def __init__(self, data_file='../data/films.json'):
        self.data_file = os.path.join(os.path.dirname(__file__), data_file)

    def get_all(self):
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save(self, films):
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(films, f, ensure_ascii=False, indent=2)

    def add(self, film):
        films = self.get_all()
        film['id'] = max([f.get('id', 0) for f in films], default=0) + 1
        film.setdefault('favorite', False)
        films.append(film)
        self.save(films)
        return film

    def delete(self, film_id):
        films = self.get_all()
        films = [f for f in films if f['id'] != film_id]
        self.save(films)

    def update(self, film_id, data):
        films = self.get_all()
        for film in films:
            if film['id'] == film_id:
                film.update(data)
                self.save(films)
                return film
        return None

    def toggle_favorite(self, film_id):
        films = self.get_all()
        for film in films:
            if film['id'] == film_id:
                film['favorite'] = not film.get('favorite', False)
                self.save(films)
                return film
        return None

    def search(self, query=None, genre=None):
        films = self.get_all()
        if query:
            query_lower = query.lower()
            films = [f for f in films if
                     query_lower in f['title'].lower() or
                     query_lower in f.get('description', '').lower()]
        if genre:
            films = [f for f in films if genre.lower() in f['genre'].lower()]
        return films


film_manager = FilmManager()

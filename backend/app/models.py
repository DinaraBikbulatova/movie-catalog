from .database import db
from datetime import datetime


class Film(db.Model):
    __tablename__ = 'films'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text, default='')
    favorite = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year,
            'genre': self.genre,
            'rating': self.rating,
            'description': self.description,
            'favorite': self.favorite
        }

    @classmethod
    def get_all(cls):
        return [film.to_dict() for film in cls.query.all()]

    @classmethod
    def add(cls, data):
        film = cls(
            title=data['title'],
            year=data['year'],
            genre=data['genre'],
            rating=data.get('rating', 0.0),
            description=data.get('description', ''),
            favorite=data.get('favorite', False)
        )
        db.session.add(film)
        db.session.commit()
        return film.to_dict()

    @classmethod
    def delete(cls, film_id):
        film = cls.query.get(film_id)
        if film:
            db.session.delete(film)
            db.session.commit()
            return True
        return False

    @classmethod
    def update(cls, film_id, data):
        film = cls.query.get(film_id)
        if film:
            for key, value in data.items():
                if hasattr(film, key):
                    setattr(film, key, value)
            db.session.commit()
            return film.to_dict()
        return None

    @classmethod
    def toggle_favorite(cls, film_id):
        film = cls.query.get(film_id)
        if film:
            film.favorite = not film.favorite
            db.session.commit()
            return film.to_dict()
        return None

    @classmethod
    def search(cls, query=None, genre=None):
        films = cls.query
        if query:
            films = films.filter(
                db.or_(
                    cls.title.ilike(f'%{query}%'),
                    cls.description.ilike(f'%{query}%')
                )
            )
        if genre:
            films = films.filter(cls.genre.ilike(f'%{genre}%'))
        return [film.to_dict() for film in films.all()]

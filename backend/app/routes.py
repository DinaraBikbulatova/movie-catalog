from flask import Blueprint, request, jsonify
from .database import db, Film

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/health')
def health():
    count = Film.query.count()
    return jsonify({
        "status": "ok",
        "database": "SQLite",
        "films_count": count
    })


@bp.route('/films', methods=['GET'])
def get_films():
    films = [film.to_dict() for film in Film.query.all()]
    return jsonify(films)


@bp.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    film = Film.query.get(film_id)
    return jsonify(film.to_dict()) if film else ('', 404)


@bp.route('/films', methods=['POST'])
def add_film():
    data = request.get_json()
    if not data.get('title') or not data.get('year') or not data.get('genre'):
        return jsonify({'error': 'Нужны title, year, genre'}), 400

    film = Film(
        title=data['title'],
        year=data['year'],
        genre=data['genre'],
        rating=data.get('rating', 0.0),
        description=data.get('description', ''),
        favorite=data.get('favorite', False)
    )
    db.session.add(film)
    db.session.commit()
    return jsonify(film.to_dict()), 201


@bp.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return '', 404

    data = request.get_json()
    for key, value in data.items():
        if hasattr(film, key) and key != 'id':
            setattr(film, key, value)

@bp.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film = Film.query.get(film_id)
    if not film:
        return '', 404

    db.session.delete(film)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Фильм удален'})


@bp.route('/films/<int:film_id>/favorite', methods=['POST'])
def toggle_favorite(film_id):
    film = Film.query.get(film_id)
    if not film:
        return '', 404

    film.favorite = not film.favorite
    db.session.commit()
    return jsonify(film.to_dict())


@bp.route('/films/search', methods=['GET'])
def search_films():
    query = request.args.get('q', '')
    genre = request.args.get('genre', '')

    films_query = Film.query

    if query:
        films_query = films_query.filter(
            db.or_(
                Film.title.ilike(f'%{query}%'),
                Film.description.ilike(f'%{query}%')
            )
        )

    if genre:
        films_query = films_query.filter(Film.genre.ilike(f'%{genre}%'))

    films = [film.to_dict() for film in films_query.all()]
    return jsonify(films)


# Дополнительный эндпоинт для получения жанров
@bp.route('/genres', methods=['GET'])
def get_genres():
    genres = db.session.query(Film.genre).distinct().all()
    return jsonify([genre[0] for genre in genres])
from flask import Blueprint, request, jsonify
from .models import film_manager

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/health')
def health():
    return jsonify({"status": "ok"})


@bp.route('/films', methods=['GET'])
def get_films():
    films = film_manager.get_all()
    return jsonify(films)


@bp.route('/films/<int:film_id>', methods=['GET'])
def get_film(film_id):
    films = film_manager.get_all()
    film = next((f for f in films if f['id'] == film_id), None)
    return jsonify(film) if film else ('', 404)


@bp.route('/films', methods=['POST'])
def add_film():
    data = request.get_json()
    if not data.get('title') or not data.get('year') or not data.get('genre'):
        return jsonify({'error': 'Нужны title, year, genre'}), 400

    film = film_manager.add(data)
    return jsonify(film), 201


@bp.route('/films/<int:film_id>', methods=['PUT'])
def update_film(film_id):
    data = request.get_json()
    film = film_manager.update(film_id, data)
    return jsonify(film) if film else ('', 404)


@bp.route('/films/<int:film_id>', methods=['DELETE'])
def delete_film(film_id):
    film_manager.delete(film_id)
    return jsonify({'message': 'Фильм удален'})


@bp.route('/films/<int:film_id>/favorite', methods=['POST'])
def toggle_favorite(film_id):
    film = film_manager.toggle_favorite(film_id)
    return jsonify(film) if film else ('', 404)


@bp.route('/films/search', methods=['GET'])
def search_films():
    query = request.args.get('q', '')
    genre = request.args.get('genre', '')
    films = film_manager.search(query, genre)
    return jsonify(films)

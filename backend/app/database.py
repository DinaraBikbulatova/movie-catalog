from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


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


def init_app(app):

    # Получаем абсолютный путь к корню проекта (tp_project)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Путь к папке data
    data_dir = os.path.join(project_root, 'data')

    # Создаем папку data, если она не существует
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        print(f"📁 Создана папка: {data_dir}")

    # Абсолютный путь к файлу базы данных
    db_path = os.path.join(data_dir, 'films.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Выводим информацию о пути к БД (для отладки)
    print(f"🗄️  База данных: {db_path}")

    db.init_app(app)

    with app.app_context():
        # Создаём все таблицы
        db.create_all()

        # Если таблица пустая - добавляем начальные данные
        if Film.query.count() == 0:
            seed_initial_data()
            print("✅ База данных инициализирована с начальными данными")
        else:
            print(f"📊 В базе уже есть {Film.query.count()} фильмов")


def seed_initial_data():
    """Добавляем начальные данные в БД"""
    initial_films = [
        {
            'title': 'Интерстеллар',
            'year': 2014,
            'genre': 'Фантастика',
            'rating': 8.6,
            'description': 'Когда засуха, пыльные бури и вымирание растений приводят человечество к продовольственному кризису, коллектив исследователей и учёных отправляется сквозь червоточину в путешествие, чтобы превзойти прежние ограничения для космических путешествий человека и найти планету с подходящими для человечества условиями.',
            'favorite': True
        },
        {
            'title': 'Начало',
            'year': 2010,
            'genre': 'Фантастика',
            'rating': 8.8,
            'description': 'Кобб — талантливый вор, лучший из лучших в опасном искусстве извлечения: он крадет ценные секреты из глубин подсознания во время сна, когда человеческий размотр наиболее уязвим.',
            'favorite': True
        },
        {
            'title': 'Побег из Шоушенка',
            'year': 1994,
            'genre': 'Драма',
            'rating': 9.3,
            'description': 'Бухгалтер Энди Дюфрейн обвинён в убийстве собственной жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он сталкивается с жестокостью и беззаконием, царящими по обе стороны решётки.',
            'favorite': False
        },
        {
            'title': 'Оно',
            'year': 2017,
            'genre': 'Ужасы',
            'rating': 7.3,
            'description': 'Когда в городке Дерри штата Мэн начинают пропадать дети, несколько ребят сталкиваются со своими величайшими страхами — не только с группой школьных хулиганов, но со злобным клоуном Пеннивайзом, список жертв которого уходит вглубь веков.',
            'favorite': False
        }
    ]

    for film_data in initial_films:
        film = Film(**film_data)
        db.session.add(film)

    db.session.commit()
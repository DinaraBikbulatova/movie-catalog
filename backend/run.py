from app import create_app

app = create_app()

if __name__ == '__main__':
    print("Сервер запущен: http://localhost:5000")
    print("API доступно по адресу: http://localhost:5000/api")
    print("База данных: SQLite (backend/data/films.db)")
    print("\nДоступные endpoints:")
    print("   GET  /api/health             - проверка работы")
    print("   GET  /api/films              - все фильмы")
    print("   POST /api/films              - добавить фильм")
    print("   PUT  /api/films/<id>         - обновить фильм")
    print("   DELETE /api/films/<id>       - удалить фильм")
    print("   POST /api/films/<id>/favorite - избранное")
    print("   GET  /api/films/search       - поиск")
    print("\nНе закрывайте это окно!")
    app.run(debug=True, port=5000)

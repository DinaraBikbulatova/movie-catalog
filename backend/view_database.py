import sqlite3
import os


def check_database():
    # Определяем путь к базе данных так же, как в database.py
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    db_path = os.path.join(data_dir, 'films.db')

    print(f"🔍 Ищу базу данных по пути: {db_path}")
    if not os.path.exists(db_path):
        print("❌ База данных не найдена!")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("🔍 ПРОВЕРКА БАЗЫ ДАННЫХ")

    # 1. Информация о базе
    cursor.execute("SELECT sqlite_version();")
    print(f"SQLite версия: {cursor.fetchone()[0]}")

    # 2. Таблицы
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"\n📋 Таблицы ({len(tables)}):")
    for table in tables:
        print(f"  • {table[0]}")

    # 3. Данные из films
    print("\n🎬 ФИЛЬМЫ:")
    cursor.execute("SELECT * FROM films ORDER BY id;")
    films = cursor.fetchall()

    if films:
        # Заголовки
        cursor.execute("PRAGMA table_info(films);")
        columns = cursor.fetchall()
        headers = [col[1] for col in columns]

        print("\n" + " | ".join(headers))
        print("-" * 80)

        for film in films:
            # Красиво форматируем
            formatted = []
            for i, value in enumerate(film):
                if headers[i] == 'favorite':
                    formatted.append('❤️' if value else '○')
                elif isinstance(value, str) and len(value) > 20:
                    formatted.append(value[:17] + '...')
                else:
                    formatted.append(str(value))
            print(" | ".join(formatted))

        print(f"\nВсего фильмов: {len(films)}")
        cursor.execute("SELECT COUNT(*) FROM films WHERE favorite = 1;")
        favorites = cursor.fetchone()[0]
        print(f"Избранных: {favorites}")
    else:
        print("Таблица films пуста!")

    # 4. Статистика
    print("\n📊 СТАТИСТИКА:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  {table[0]}: {count} записей")

    conn.close()
    print("\n✅ Проверка завершена")


if __name__ == "__main__":
    check_database()
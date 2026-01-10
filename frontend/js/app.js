// ========== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ==========
let films = [];

// ========== ОСНОВНЫЕ ФУНКЦИИ ==========

// Загрузить и отобразить фильмы
async function loadFilms() {
    try {
        console.log("Загружаем фильмы...");
        films = await api.getFilms();
        console.log("Загружено фильмов:", films.length);
        displayFilms(films);
    } catch (error) {
        console.error("Ошибка загрузки фильмов:", error);
        alert('❌ Не удалось загрузить фильмы. Проверьте сервер.');
    }
}

// Отобразить фильмы
function displayFilms(filmsToDisplay) {
    const container = document.getElementById('filmsList');
    const countElement = document.getElementById('filmsCount');
    
    countElement.textContent = filmsToDisplay.length;
    
    if (filmsToDisplay.length === 0) {
        container.innerHTML = `
            <div class="card" style="text-align: center; padding: 40px; grid-column: 1 / -1;">
                <i class="fas fa-film fa-3x" style="color: #bdc3c7; margin-bottom: 20px;"></i>
                <h3>Фильмы не найдены</h3>
                <p>Добавьте первый фильм</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    filmsToDisplay.forEach(film => {
        html += `
            <div class="film-card" data-id="${film.id}">
                <div class="film-header">
                    <div class="film-title">${film.title}</div>
                    <div class="film-year">${film.year}</div>
                </div>
                
                <div class="film-genre">${film.genre}</div>
                
                ${film.rating ? `
                    <div class="film-rating">⭐ ${film.rating}/10</div>
                ` : ''}
                
                ${film.description ? `
                    <div class="film-description">${film.description}</div>
                ` : ''}
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Функция инициализации
async function initApp() {
    console.log("Страница загружена, проверяем подключение...");
    
    // Проверяем подключение к API
    const isConnected = await api.checkHealth();
    console.log("API подключен:", isConnected);
    
    if (!isConnected) {
        alert('⚠️ Сервер не запущен!\n\nЗапустите бэкенд командой:\n\ncd backend\npython run.py');
        return;
    }
    
    // Загружаем фильмы
    await loadFilms();
    console.log("Фильмы загружены:", films.length);
}

// Запускаем инициализацию при загрузке страницы
document.addEventListener('DOMContentLoaded', initApp);

// Добавить фильм
async function addFilm() {
    console.log("Добавление фильма...");
    
    const title = document.getElementById('title').value.trim();
    const year = document.getElementById('year').value;
    const genre = document.getElementById('genre').value.trim();
    const rating = document.getElementById('rating').value;
    const description = document.getElementById('description').value.trim();
    
    // Валидация
    if (!title) {
        alert('⚠️ Введите название фильма');
        document.getElementById('title').focus();
        return;
    }
    
    if (!year || year < 1900 || year > 2024) {
        alert('⚠️ Введите корректный год (1900-2024)');
        document.getElementById('year').focus();
        return;
    }
    
    if (!genre) {
        alert('⚠️ Введите жанр фильма');
        document.getElementById('genre').focus();
        return;
    }
    
    // Создаем объект фильма
    const film = {
        title: title,
        year: parseInt(year),
        genre: genre,
        rating: rating ? parseFloat(rating) : 0,
        description: description,
        favorite: false
    };
    
    console.log("Добавляем фильм:", film);
    
    try {
        // Отправляем на сервер
        const result = await api.addFilm(film);
        console.log("Фильм добавлен:", result);
        
        // Очищаем форму
        document.getElementById('title').value = '';
        document.getElementById('year').value = '';
        document.getElementById('genre').value = '';
        document.getElementById('rating').value = '';
        document.getElementById('description').value = '';
        
        // Обновляем список фильмов
        await loadFilms();
        
        // Показываем уведомление
        alert('✅ Фильм успешно добавлен!');
        
    } catch (error) {
        console.error("Ошибка при добавлении фильма:", error);
        alert('❌ Не удалось добавить фильм. Проверьте сервер.');
    }
}

// Экспортируем функцию в глобальную область
window.addFilm = addFilm;

// ========== УПРАВЛЕНИЕ ФИЛЬМАМИ ==========
let editingFilmId = null;

// Обновляем функцию displayFilms для добавления кнопок
function displayFilms(filmsToDisplay) {
    const container = document.getElementById('filmsList');
    const countElement = document.getElementById('filmsCount');
    
    countElement.textContent = filmsToDisplay.length;
    
    if (filmsToDisplay.length === 0) {
        container.innerHTML = `
            <div class="card" style="text-align: center; padding: 40px; grid-column: 1 / -1;">
                <i class="fas fa-film fa-3x" style="color: #bdc3c7; margin-bottom: 20px;"></i>
                <h3>Фильмы не найдены</h3>
                <p>${showOnlyFavorites ? 'Добавьте фильмы в избранное' : 'Добавьте первый фильм'}</p>
            </div>
        `;
        return;
    }
    
    let html = '';
    
    filmsToDisplay.forEach(film => {
        html += `
            <div class="film-card ${film.favorite ? 'favorite' : ''}" data-id="${film.id}">
                <div class="film-header">
                    <div class="film-title">${film.title}</div>
                    <div class="film-year">${film.year}</div>
                </div>
                
                <div class="film-genre">${film.genre}</div>
                
                ${film.rating ? `
                    <div class="film-rating">⭐ ${film.rating}/10</div>
                ` : ''}
                
                ${film.description ? `
                    <div class="film-description">${film.description}</div>
                ` : ''}
                
                <div class="film-actions">
                    <button class="fav-btn ${film.favorite ? 'favorited' : ''}" 
                            onclick="toggleFavorite(${film.id})">
                        <i class="fas fa-heart"></i> 
                        ${film.favorite ? 'В избранном' : 'В избранное'}
                    </button>
                    <button class="edit-btn" onclick="openEditModal(${film.id})">
                        <i class="fas fa-edit"></i> Редактировать
                    </button>
                    <button class="delete-btn" onclick="deleteFilm(${film.id})">
                        <i class="fas fa-trash"></i> Удалить
                    </button>
                </div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}

// Удалить фильм
async function deleteFilm(id) {
    if (!confirm('Вы уверены, что хотите удалить этот фильм?')) {
        return;
    }
    
    console.log("Удаление фильма ID:", id);
    
    try {
        await api.deleteFilm(id);
        console.log("Фильм удален");
        
        // Обновляем список фильмов
        await loadFilms();
        
        alert('✅ Фильм удален');
    } catch (error) {
        console.error("Ошибка при удалении фильма:", error);
        alert('❌ Не удалось удалить фильм');
    }
}

// Переключить избранное
async function toggleFavorite(id) {
    console.log("Переключение избранного для ID:", id);
    
    try {
        const updatedFilm = await api.toggleFavorite(id);
        console.log("Фильм обновлен:", updatedFilm);
        
        // Обновляем список фильмов
        await loadFilms();
        
    } catch (error) {
        console.error("Ошибка при обновлении избранного:", error);
        alert('❌ Не удалось обновить избранное');
    }
}

// Открыть модальное окно редактирования
async function openEditModal(id) {
    console.log("Открытие редактора для ID:", id);
    
    // Находим фильм
    const film = films.find(f => f.id === id);
    if (!film) {
        alert('Фильм не найден');
        return;
    }
    
    // Сохраняем ID редактируемого фильма
    editingFilmId = id;
    
    // Заполняем форму редактирования
    document.getElementById('editTitle').value = film.title;
    document.getElementById('editYear').value = film.year;
    document.getElementById('editGenre').value = film.genre;
    document.getElementById('editRating').value = film.rating || '';
    document.getElementById('editDescription').value = film.description || '';
    
    // Показываем модальное окно
    document.getElementById('editModal').style.display = 'flex';
}

// Сохранить изменения
async function saveFilm() {
    if (!editingFilmId) return;
    
    console.log("Сохранение изменений для ID:", editingFilmId);
    
    // Получаем данные из формы
    const film = {
        title: document.getElementById('editTitle').value.trim(),
        year: parseInt(document.getElementById('editYear').value),
        genre: document.getElementById('editGenre').value.trim(),
        rating: parseFloat(document.getElementById('editRating').value) || 0,
        description: document.getElementById('editDescription').value.trim()
    };
    
    // Валидация
    if (!film.title || !film.year || !film.genre) {
        alert('Заполните все обязательные поля');
        return;
    }
    
    try {
        // Сохраняем изменения
        await api.updateFilm(editingFilmId, film);
        console.log("Фильм обновлен");
        
        // Закрываем модальное окно
        closeModal();
        
        // Обновляем список фильмов
        await loadFilms();
        
        alert('✅ Фильм успешно обновлен!');
        
    } catch (error) {
        console.error("Ошибка при обновлении фильма:", error);
        alert('❌ Не удалось обновить фильм');
    }
}

// Закрыть модальное окно
function closeModal() {
    document.getElementById('editModal').style.display = 'none';
    editingFilmId = null;
    
    // Очищаем форму
    document.getElementById('editTitle').value = '';
    document.getElementById('editYear').value = '';
    document.getElementById('editGenre').value = '';
    document.getElementById('editRating').value = '';
    document.getElementById('editDescription').value = '';
}

// Экспортируем функции
window.deleteFilm = deleteFilm;
window.toggleFavorite = toggleFavorite;
window.openEditModal = openEditModal;
window.saveFilm = saveFilm;
window.closeModal = closeModal;

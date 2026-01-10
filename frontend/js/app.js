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

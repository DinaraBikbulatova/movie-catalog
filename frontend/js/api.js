// API конфигурация
const API_URL = 'http://localhost:5000/api';

// Все API функции
const api = {
    // Получить все фильмы
    async getFilms() {
        const response = await fetch(`${API_URL}/films`);
        return await response.json();
    },

    // Добавить фильм
    async addFilm(film) {
        const response = await fetch(`${API_URL}/films`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(film)
        });
        return await response.json();
    },

    // Обновить фильм
    async updateFilm(id, film) {
        const response = await fetch(`${API_URL}/films/${id}`, {
            method: 'PUT',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(film)
        });
        return await response.json();
    },

    // Удалить фильм
    async deleteFilm(id) {
        await fetch(`${API_URL}/films/${id}`, {
            method: 'DELETE'
        });
    },

    // Переключить избранное
    async toggleFavorite(id) {
        const response = await fetch(`${API_URL}/films/${id}/favorite`, {
            method: 'POST'
        });
        return await response.json();
    },

    // Проверить здоровье API
    async checkHealth() {
        try {
            const response = await fetch(`${API_URL}/health`);
            return response.ok;
        } catch {
            return false;
        }
    }
};

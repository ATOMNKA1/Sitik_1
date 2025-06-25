const API_URL = 'http://127.0.0.1:8000';

async function apiRequest(url, method = 'GET', data = null, token = null, contentType = 'application/json') {
    const headers = {};
    if (contentType) {
        headers['Content-Type'] = contentType;
    }
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const config = { method, headers };
    if (data) {
        if (contentType === 'application/x-www-form-urlencoded') {
            const formData = new URLSearchParams();
            for (const key in data) {
                formData.append(key, data[key]);
            }
            config.body = formData;
        } else {
            config.body = JSON.stringify(data);
        }
    }
    const response = await fetch(`${API_URL}${url}`, config);
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Ошибка запроса: ${response.status}`);
    }
    return response.status === 204 ? null : response.json();
}

// Аутентификация
function register(data) {
    return apiRequest('/register', 'POST', data);
}

function login(data) {
    return apiRequest('/token', 'POST', data, null, 'application/x-www-form-urlencoded');
}

function adminLogin(data) {
    return apiRequest('/admin/login', 'POST', data, null, 'application/x-www-form-urlencoded');
}

// Игры
function getGames(skip = 0, limit = 10, name = '') {
    return apiRequest(`/games?skip=${skip}&limit=${limit}${name ? `&name=${name}` : ''}`);
}

function getGame(id) {
    return apiRequest(`/games/${id}`);
}

function createGame(data, token) {
    return apiRequest('/games', 'POST', data, token);
}

function updateGame(id, data, token) {
    return apiRequest(`/games/${id}`, 'PUT', data, token);
}

function deleteGame(id, token) {
    return apiRequest(`/games/${id}`, 'DELETE', null, token);
}

// Комментарии
function getComments(gameId, skip = 0, limit = 10) {
    return apiRequest(`/games/${gameId}/comments?skip=${skip}&limit=${limit}`);
}

function createComment(gameId, data, token) {
    return apiRequest(`/games/${gameId}/comments`, 'POST', data, token);
}

function updateComment(id, data, token) {
    return apiRequest(`/comments/${id}`, 'PUT', data, token);
}

function deleteComment(id, token) {
    return apiRequest(`/comments/${id}`, 'DELETE', null, token);
}

// Избранное
function getFavorites(token, skip = 0, limit = 10) {
    return apiRequest(`/favorites?skip=${skip}&limit=${limit}`, 'GET', null, token);
}

function addFavorite(data, token) {
    return apiRequest('/favorites', 'POST', data, token);
}

function isFavorited(gameId, token) {
    return apiRequest(`/favorites/is_favorited?game_id=${gameId}`, 'GET', null, token);
}

function removeFavorite(gameId, token) {
    return apiRequest(`/favorites/${gameId}`, 'DELETE', null, token);
}

// Пользователи
function getUser(id, token) {
    return apiRequest(`/users/${id}`, 'GET', null, token);
}

function getUserByLogin(login, token) {
    return apiRequest(`/users/by-login/${login}`, 'GET', null, token);
}

function updateUser(id, data, token) {
    return apiRequest(`/users/${id}`, 'PUT', data, token);
}

function deleteUser(id, token) {
    return apiRequest(`/users/${id}`, 'DELETE', null, token);
}

function getAllUsers(skip = 0, limit = 10, token) {
    return apiRequest(`/users?skip=${skip}&limit=${limit}`, 'GET', null, token);
}
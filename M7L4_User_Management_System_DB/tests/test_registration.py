import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Фикстура для настройки базы данных перед тестами и её очистки после."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Фикстура для получения соединения с базой данных и его закрытия после теста."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(connection):
    """Тест создания базы данных и таблицы пользователей."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Таблица 'users' должна существовать в базе данных."

def test_add_new_user(connection):
    """Тест добавления нового пользователя."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Пользователь должен быть добавлен в базу данных."

def test_add_existing_user():
    user = add_user('testuser', 'testuser@example.com', 'password123')
    assert not user, "Добавление существующего пользователя должно вернуть None."

def test_authenticate_user():
    result = authenticate_user('testuser', 'password123')
    assert result, "Аутентификация должна пройти успешно для существующего пользователя."

def test_authenticate_nonexistent_user(setup_database):
    result = authenticate_user('nonexistentuser', 'password123')
    assert not result, "Аутентификация несуществующего пользователя должна вернуть None."

def test_authenticate_user_with_wrong_password(setup_database):    
    result = authenticate_user('testuser', 'wrongpassword')
    assert not result, "Аутентификация с неправильным паролем должна вернуть None."

def test_display_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    assert len(users) > 0, "Список пользователей должен содержать хотя бы одного пользователя."


# Возможные варианты тестов:
"""
Тест добавления пользователя с существующим логином.
Тест успешной аутентификации пользователя.
Тест аутентификации несуществующего пользователя.
Тест аутентификации пользователя с неправильным паролем.
Тест отображения списка пользователей.
"""
Book Store - Django приложение
Book Store — это комплексное Django-приложение для управления книжным магазином, включающее инвентаризацию, отслеживание продаж, генерацию отчетов и обработку заказов.

Возможности

Управление книгами: Добавление, редактирование и удаление книг

Управление жанрами: Создание и управление книжными жанрами

Система заказов: Отслеживание заказов и управление запасами

Аналитика продаж:

Статистика по авторам и их прибыльности
Отслеживание стоимости продаж
Анализ маржи прибыли
Поиск и фильтрация: Поиск книг по названию, автору или жанру
Пагинация: Удобная навигация по большим каталогам книг
Аутентификация пользователей: Защищенный интерфейс администратора

Установка

Предварительные требования
Python 3.8+
Django 4.0+
SQLite (или другая поддерживаемая СУБД)

Шаги установки

Клонируйте репозиторий:

bash
git clone https://github.com/yourusername/book_store.git
cd book_store

Создайте виртуальное окружение:

bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Установите зависимости:

bash
pip install -r requirements.txt

Примените миграции:

bash
python manage.py migrate

Создайте суперпользователя:

bash
python manage.py createsuperuser

Запустите сервер разработки:

bash
python manage.py runserver

Структура проекта

book_store/
├── books/                     # Основное приложение
│   ├── migrations/            # Миграции базы данных
│   ├── templates/             # HTML-шаблоны
│   ├── __init__.py
│   ├── admin.py               # Конфигурация админки
│   ├── apps.py                # Конфигурация приложения
│   ├── forms.py               # Формы
│   ├── models.py              # Модели данных
│   ├── tests.py               # Юнит-тесты
│   ├── urls.py                # Маршрутизация приложения
│   └── views.py               # Функции представлений
├── book_store/                # Конфигурация проекта
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Настройки проекта
│   ├── urls.py                # Основная маршрутизация
│   └── wsgi.py
├── static/                    # Статические файлы (CSS, JS, изображения)
└── manage.py                  # Скрипт управления Django

Ключевые компоненты

Модели
Book: Представляет книги с детальной информацией
Genre: Категории книг
Order: Отслеживает заказы книг

Представления
Управление книгами (добавление, редактирование, удаление)
Управление жанрами
Обработка заказов
Аналитика продаж и отчеты
Статистика по авторам

Шаблоны
Адаптивные HTML-шаблоны с использованием Django Template Language
Каталог книг с возможностями фильтрации
Формы для ввода данных
Отчеты и статистика

Использование
Доступ к приложению

После запуска сервера приложение доступно по адресу:


http://localhost:8000/
Интерфейс администратора

Доступ к админке:

http://localhost:8000/admin/
Используйте учетные данные суперпользователя, созданные при установке.

Основные функции
Каталог книг: Просмотр книг с фильтрацией

Добавление книг: Создание новых записей о книгах

Управление жанрами: Создание и редактирование жанров книг

Система заказов: Отслеживание книжных заказов

Отчеты:

Статистика по авторам
Продажи
Прибыль

Тестирование
Запуск тестов

bash
python manage.py test books

Покрытие тестами
Тестовый набор охватывает:

CRUD-операции с книгами
Управление жанрами
Обработку заказов
Статистические расчеты
Валидацию форм

End-to-End тестирование с помощью Cypress

Проект включает тесты Cypress для критически важных сценариев:

Запуск тестов Cypress
Установите Cypress:

bash
npm install cypress --save-dev
Запустите Django-сервер:

bash
python manage.py runserver

Запустите Cypress:

bash
npx cypress open

Ключевые тестовые сценарии

Аутентификация пользователя
Добавление книг из фикстур
Валидация форм
Проверка CSRF-токенов
Редиректы после отправки форм

Конфигурация
Ключевые настройки в book_store/settings.py:

Конфигурация базы данных
Настройка статических файлов
Настройки аутентификации
Конфигурация middleware
Настройки шаблонов

Участие в проекте
Мы приветствуем ваш вклад! Пожалуйста, следуйте следующим шагам:

Сделайте форк репозитория
Создайте новую ветку для вашей функции
Зафиксируйте ваши изменения
Запушьте изменения в ваш форк
Создайте pull request


Автор
Кузнецов Матвей

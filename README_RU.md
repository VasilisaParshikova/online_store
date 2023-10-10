# Онлайн магазин музыкальных товаров

Целью проекта было создать функциональный маркетплайс музыкальных товаров.

Проект состоить из трёх приложений:
- shop_app (вся логика связанная с каталогом и страницами товара)
- orders_app (вся логика связанная с корзиной, оформлением и оплатой заказов, историей заказов)
- user_app (вся логика связанная с личными данными пользователей, регистрацией, аутентификацией)

Сайт имеет следущую функциональность:
- Каталог товаров
- Поиск и фильтрация товаров в каталоге
- Страница просмотра детальной информации о товаре
- Добавление товара в корзину по кнопкам со страницы каталога и со страницы товара
- Возможность просмотреть товар в корзине, удалить товар из корзины, поменять количество товара в корзине
- Реализован личный кабинет покупателя
- Оформление и оплата (заглушка) заказа
- Просмотр истории заказов
- Регистрация и аутентификация пользователей
- Все функции сайта до оформления и оплаты заказа возможны для незарегистрированных пользователей. Реализована возможность регистрации или аутентификации на первом этапе оформления заказа. При входе на сайт или регистрации все товары, добавленные в корзину до момента аутентификации автоматически переносятся в корзину пользователя.
- Настроена административная панель.

### Мой вклад
В данном проекте мною реализовывался бекэнд от проектирования страктуры приложений, ссылок и БД проекта до реализации скриптов всех функций сайта. Также при необходимости вносила некоторые дополнения и корректировки в предоставленный фронтенд сайта.

### Использованный стек
Python 3.9

Django 4.1.7

База данных - использовалась встроенная ORM Django и идущая по умолчанию БД sqlite

Для развёртывания проекта подготовлены файлы:
- requirements.txt
- папка fixtures со всем необходимым для демонстрации работы проекта фикстурами данных 
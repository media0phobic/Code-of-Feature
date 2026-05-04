# Code-of-Feature
# Currency Converter

Автор: [Александр Шалаев]

## Как получить API-ключ

1. Зарегистрируйтесь на exchangerate-api.com.
2. Получите API-ключ в личном кабинете.
3. Вставьте ключ в переменную `API_KEY` в начале файла `currency_converter.py`.

## Запуск приложения

1. Установите зависимости:
   pip install -r requirements.txt

2. Запустите приложение:
   python currency_converter.py

## История операций

История сохраняется в файл `history.json` и отображается в таблице при запуске.

# Инициализация Git и отправка на удалённый репозиторий

git init
git add .
git commit -m "Initial commit"
git remote add origin <ссылка_на_репозиторий>
git push -u origin master

### Запуск приложения

1. Установите зависимости: pip install -r requirements.txt
2. Запустите приложение: flask run
3. Откройте браузер и отправьте POST-запрос на http://127.0.0.1:5000/process с необходимыми параметрами.

Пример запроса:
```
curl -X POST http://127.0.0.1:5000/process \
 -H 'api_key: YOUR_API_KEY' \
 -F 'image=@tests/test.jpg' \
 -F 'operation=resize' \
 -F 'width=100' \
 -F 'height=100'
```
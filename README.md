# Нагрузочное тестирование API

Скрипт асинхронно и последовательно отправляет POST-запросы на следующие адреса:
 - https://api.denumpay.ru/test/hs/api/v1/payment/ia/new
 - https://api.denumpay.ru/test/hs/api/v1/payment/ia/pay?paymentId=<paymentId>

## Установка:

1. Обновление пакетного менеджера `pip`:

   ```bash
   python3 -m pip install --upgrade pip
   ```

1. Установка виртуального окружения `venv`:

   ```bash
   python3 -m venv venv
   ```

1. Активация виртуального окружения:

   - для linux:
   ```bash
   source venv/bin/activate
   ```
   - для Windows:
   ```bash
   .\venv\Scripts\activate.ps1
   ```

1. Установка пакетов из `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

## Настройки:
Все настройки находятся в `conf.py`:

 - `limit_of_connections` - число одновременных запросов
 - `number_of_requests` - общее число запросов 

Пример заполнения:
    
```python
limit_of_connections = 1000
number_of_requests = 10000
token = '***'
```

## Запуск:

```bash
python3 async_test_api.py
```



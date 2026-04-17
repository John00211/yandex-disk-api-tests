\# Тестовый проект: API‑тесты Яндекс.Диска



Это небольшой проект автотестов для REST API Яндекс.Диска.  

Тесты написаны на Python3, с использованием Pytest и requests.



\## Что в проекте



\- Тесты для GET, POST, PUT и DELETE запросов к Яндекс.Диску.  

\- Примеры работы с папками и файлами (создание, переименование, удаление).  

\- Токен OAuth передаётся через параметр --token или переменную окружения, его нет в коде.

## Структура проекта







\## Как запустить



1\. Открой папку проекта в терминале:

&#x20;  ```bash

&#x20;  cd yandex-disk-api-tests

&#x20;  ```



2\. Создай и активируй виртуальное окружение:

&#x20;  ```bash

&#x20;  python3 -m venv venv

&#x20;  source venv/bin/activate    # Linux / macOS

&#x20;  venv\\Scripts\\activate        # Windows

&#x20;  ```



3\. Установи зависимости:

&#x20;  ```bash

&#x20;  pip install -r requirements.txt

&#x20;  ```



4\. Получи OAuth‑токен через полигон Яндекс.Диска:

&#x20;  - https://yandex.ru/dev/disk/poligon/



5\. Запусти тесты с токеном:

&#x20;  ```bash

&#x20;  pytest -v --token="OAuth...your\_token\_here"

&#x20;  ```



Если нужно, можно передать токен через переменную окружения:

```bash

export YANDEX\_DISK\_TOKEN="OAuth...your\_token\_here"

pytest -v

```



Таким образом проект выполняет тестовое задание:

\- запускается локально,

\- использует Python3 + Pytest + requests,

\- покрывает GET, POST, PUT и DELETE методы API Яндекс.Диска.


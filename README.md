# Парсер сайта государственных закупок (ЕИС)

## Предварительные условия:

Во время разработки использовалась система Ubuntu 20.04.6 LTS
на которой были установлены [python](https://www.python.org/), [docker](https://www.docker.com/) и [git](https://git-scm.com/)

## Запуск

1. Создать новую директорию `mkdir dir`
2. Перейти в созданную директорию `cd dir`
3. Клонировать реппозиторий `git clone https://github.com/Z9121/eis.git`
4. Перейти в директорию `cd eis`
5. Выполнить команду `docker-compose up` и дождаться запуска контейнеров (в этом окне можно будет наблюдать за выводом воркера после запуска парсера)
6. В новом окне терминала выполнить команду `docker exec -d producer python parser/parser.py`
7. Для выполнения тестов в этом же окне выполнить команду `docker exec producer pytest`

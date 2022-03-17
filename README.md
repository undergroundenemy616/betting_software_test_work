# Тестовое задание для Betting Software

## Cтек:

Python 3.9, Fast Api, MongoDB, Nginx, Docker.

## Как запустить проект:

После клонирования проекта локально необходимо выполнить команды:
```
docker-compose --env-file=src/.env up -d
bash setupDB.sh
```

## Про хранилище:

Для реализации задания было выбрана MongoDB в качестве базы данных. База шардируется двумя нодами, каждая нода имеет по 3 реплики.

## Про отказоустойчивость:
Для всех запросов к базе применем паттерн back-off.

## Про CI/CD:
Было реализовано несколько github actions:
1) Билд и пуш образа в Docker Hub при пуше в ветки master/production.
2) Анализ кода линтером flake8 при пул реквесте в ветки master/production
3) Ручной деплой приложения ветки master/production. Все переменные окружения для деплоя (ip хоста, ssh юзернейм, ssh port и т.д.) должны указываться в вспомогательном репозитории для деплоя (https://github.com/undergroundenemy616/betting_software_test_work_deploy).

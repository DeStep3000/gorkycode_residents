# gorkycode_residents
Решение кейса по GORKYCODE "Заявки жителей"

1 - Клонируем репозиторий

2 - Создаем венв для бэка:

```bash
cd backend
uv sync
.venv/Scripts/activate
```

2* - Чтобы подсвечивать синтаксис, выбираем интерпретатор дял проекта - венв с бэка, папку backend делаем - source. папку frontend - exclude

2** - Нужно самому разобраться, как у тебя в иде добавить node в путь папки frontend

3 - Оставляем открытой консоль для бэка, открываем новую консоль и делаем венв для фронта:

```bash
cd frontend
npm install
npm -v
node -v
```

4 - Теперь заходим в консоль для бэка, запускаем докер и вручную вставляем миграцию, чтобы протестить:

``` bash
docker compose build
docker compose up -d
```

``` bash
docker exec -it portal-db bash
psql -U portal -d portal
```

``` bash
INSERT INTO service (id, name, address, phone)
VALUES
    (1, 'Управление дорог', 'ул. Центральная 12', '+7 900 000-00-01'),
    (2, 'Управление освещения', 'ул. Светлая 5', '+7 900 000-00-02'),
    (3, 'Управление благоустройства', 'ул. Парковая 3', '+7 900 000-00-03')
ON CONFLICT (id) DO NOTHING;
```

``` bash
INSERT INTO category (id, name, service_id)
VALUES
    (1, 'Дороги', 1),
    (2, 'Освещение', 2),
    (3, 'Мусор', 3)
ON CONFLICT (id) DO NOTHING;
```

``` bash
\q
exit
```

5 - Нужно перезапустить контейнер, чтобы получить актуальную бд:

``` bash
docker compose down
docker compose build
docker compose up -d
```

6 - Возвращаемся в консоль для фронта и запускаем фронт:

``` bash
npm run dev
```

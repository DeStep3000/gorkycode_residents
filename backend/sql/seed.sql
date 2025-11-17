INSERT INTO service (id, name, address, phone)
VALUES
    (1, 'Управление дорог', 'ул. Центральная 12', '+7 900 000-00-01'),
    (2, 'Управление освещения', 'ул. Светлая 5', '+7 900 000-00-02'),
    (3, 'Управление благоустройства', 'ул. Парковая 3', '+7 900 000-00-03')
ON CONFLICT (id) DO NOTHING;

INSERT INTO category (id, name, service_id)
VALUES
    (1, 'Дороги', 1),
    (2, 'Освещение', 2),
    (3, 'Мусор', 3)
ON CONFLICT (id) DO NOTHING;

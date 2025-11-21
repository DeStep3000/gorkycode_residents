-- ============================
-- EXECUTORS
-- ============================

CREATE TABLE IF NOT EXISTS executors (
    executor_id  BIGSERIAL PRIMARY KEY,
    name         VARCHAR(255) NOT NULL,
    organization VARCHAR(255),
    phone        VARCHAR(50),
    email        VARCHAR(255),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE
);

-- ============================
-- COMPLAINTS
-- ============================
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id     BIGSERIAL PRIMARY KEY,
    created_at       TIMESTAMP NOT NULL DEFAULT NOW(),
    execution_date   TIMESTAMP,
    final_status_at  TIMESTAMP,
    status           VARCHAR(50) NOT NULL,
    executor_id      BIGINT REFERENCES executors(executor_id),
    district         VARCHAR(255),
    description      TEXT NOT NULL,
    resolution       TEXT
);

CREATE INDEX IF NOT EXISTS idx_complaints_created_at
    ON complaints (created_at);

CREATE INDEX IF NOT EXISTS idx_complaints_executor_id
    ON complaints (executor_id);
-- ============================
-- MODERATORS
-- ============================

CREATE TABLE IF NOT EXISTS moderators (
    moderator_id BIGSERIAL PRIMARY KEY,
    username     VARCHAR(255) NOT NULL UNIQUE,
    full_name    VARCHAR(255) NOT NULL,
    email        VARCHAR(255),
    phone        VARCHAR(50),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    complaint_id BIGINT REFERENCES complaints(complaint_id)
);





-- ============================
-- TICKETSTATUSES
-- ============================

CREATE TABLE IF NOT EXISTS ticket_statuses (
    status_code  VARCHAR(50) NOT NULL,
    complaint_id BIGINT NOT NULL REFERENCES complaints(complaint_id) ON DELETE CASCADE,
    sort_order   INT NOT NULL,
    description  TEXT,
    data         TIMESTAMP NOT NULL,
    PRIMARY KEY (status_code, complaint_id, data)
);

CREATE INDEX IF NOT EXISTS idx_ticket_statuses_complaint_id
    ON ticket_statuses (complaint_id);



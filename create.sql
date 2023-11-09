CREATE TABLE IF NOT EXISTS count
    (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255),
        uuid  UUID,
        UNIQUE (uuid)
    )
;
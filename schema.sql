CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS persons (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),
    
    first_name VARCHAR(128) NOT NULL,
    middle_name VARCHAR(128),
    last_name VARCHAR(128) NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS segments (
    id UUID NOT NULL DEFAULT uuid_generate_v4(),

    person_id UUID NOT NULL REFERENCES persons,
    start_date DATE NOT NULL,
    end_date DATE,
    city VARCHAR(128) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (id),
    CHECK (start_date < end_date)
);
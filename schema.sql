CREATE TABLE IF NOT EXISTS persons (
    id UUID NOT NULL,
    
    first_name VARCHAR(128) NOT NULL,
    middle_name VARCHAR(128),
    last_name VARCHAR(128) NOT NULL,
    email VARCHAR(128) NOT NULL,
    date_of_birth DATE NOT NULL,

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS address_segments (
    id UUID NOT NULL,

    person_id UUID NOT NULL,

    start_date DATE NOT NULL,
    end_date DATE,

    street_one VARCHAR(128) NOT NULL,
    street_two VARCHAR(128),
    city VARCHAR(128) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code VARCHAR(10) NOT NULL,

    PRIMARY KEY (id),

    FOREIGN KEY (person_id) REFERENCES persons (id),
    
    CHECK (start_date < end_date),

	UNIQUE (person_id, start_date),
	UNIQUE (person_id, end_date)
);

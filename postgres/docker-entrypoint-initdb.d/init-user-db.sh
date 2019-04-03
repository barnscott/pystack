#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE bulletin (
        bulletin_serial serial PRIMARY KEY,
        subject VARCHAR (50) NOT NULL,
        message VARCHAR (100) NOT NULL,
        created_on TIMESTAMP NOT NULL
    );
    INSERT INTO bulletin VALUES
    (DEFAULT,'New subject','This is a test message.',current_timestamp);

    CREATE TABLE users (
        users_serial serial PRIMARY KEY,
        username VARCHAR (50) UNIQUE NOT NULL,
        password VARCHAR (100) UNIQUE NOT NULL,
        created_on TIMESTAMP NOT NULL
    );

    CREATE TABLE blog (
        blog_serial serial PRIMARY KEY,
        title VARCHAR (50) NOT NULL,
        content VARCHAR (1000) NOT NULL,
        created_on TIMESTAMP NOT NULL
    );
    INSERT INTO blog VALUES
    (DEFAULT,'First blog post','I did so much this week. Like omg, right?',current_timestamp);

EOSQL

# INSERT INTO users VALUES
# (DEFAULT,'barn','password',current_timestamp);

#INSERT INTO users (username, created_on)
#VALUES ('fred', current_timestamp;
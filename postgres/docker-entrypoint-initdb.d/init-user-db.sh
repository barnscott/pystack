#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE groups (
        group_id INTEGER PRIMARY KEY,
        created_on TIMESTAMP NOT NULL,
        groupname VARCHAR (50) UNIQUE NOT NULL
    );
    CREATE TABLE users (
        user_id serial PRIMARY KEY,
        group_id INTEGER NOT NULL DEFAULT 100,
        created_on TIMESTAMP NOT NULL,
        modified_on TIMESTAMP NOT NULL,
        username VARCHAR (50) UNIQUE NOT NULL,
        password VARCHAR (100) NOT NULL,
        FOREIGN KEY (group_id) REFERENCES groups (group_id)
    );
    CREATE TABLE bulletins (
        bulletin_id serial PRIMARY KEY,
        created_on TIMESTAMP NOT NULL,
        modified_on TIMESTAMP NOT NULL,
        subject VARCHAR (100) NOT NULL,
        content VARCHAR (5000) NOT NULL,
        due_date  TIMESTAMP NOT NULL
        
    );
    CREATE TABLE blogs (
        blog_id serial PRIMARY KEY,
        created_on TIMESTAMP NOT NULL,
        modified_on TIMESTAMP NOT NULL,
        subject VARCHAR (100) NOT NULL,
        content VARCHAR (5000) NOT NULL
    );

    INSERT INTO groups (group_id, created_on, groupname)
    VALUES  (0,current_timestamp,'admin'),
            (1,current_timestamp,'manager'),
            (100,current_timestamp,'member');

    INSERT INTO bulletins
    VALUES  (DEFAULT,current_timestamp,current_timestamp,
            'First News Bulletin',
            'This is a message to confirm that news bulletins are working. Thank you for visiting!',
            current_timestamp + interval '1 day');

    INSERT INTO blogs 
    VALUES  (DEFAULT,current_timestamp,current_timestamp,
            'First blog post',
            'I did so much this week. Like omg, right? The first thing I did was I went down to the beach and bough some bananas.');

EOSQL

# INSERT INTO users VALUES
# (DEFAULT,'barn','password',current_timestamp);

#INSERT INTO users (username, created_on)
#VALUES ('fred', current_timestamp;
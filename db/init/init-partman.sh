#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER kniffel with encrypted password 'docker';
    CREATE DATABASE kniffel ;
    GRANT ALL PRIVILEGES ON DATABASE kniffel TO kniffel;
    \connect kniffel
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO kniffel;
EOSQL


psql -v ON_ERROR_STOP=1 --username "kniffel" --dbname "kniffel" <<-EOSQL
    CREATE TABLE spieler(id SERIAL PRIMARY KEY,
                       name varchar);
    CREATE TABLE spiel(id smallint,
                       spielerId smallint,
                       advancedId smallint,
                       datum timestamp,
                       nr1 smallint,
                       nr2 smallint,
                       nr3 smallint,
                       nr4 smallint,
                       nr5 smallint,
                       nr6 smallint,
                       Zwischensumme smallint GENERATED ALWAYS AS (nr1 + nr2 + nr3 + nr4 + nr5 + nr6) STORED,
                       Bonus smallint,
                       paar1 smallint,
                       paar2 smallint,
                       gleiche3 smallint,
                       gleiche4 smallint,
                       Kuchen smallint,
                       Chance smallint,
                       Pasch smallint,
                       Zwischensumme2 smallint GENERATED ALWAYS AS (Bonus + paar1 + paar2 + gleiche3 + gleiche4 + Kuchen + Chance + Pasch) STORED,
                       Gesamtsumme smallint);


Insert into Spieler(name) values('Grit');
Insert into Spieler(name) values('Christian');
    Create view summen as

    select
      spieler.name,
      SUM(nr1) as nr1,
      SUM(nr2) as nr2,
      SUM(nr3) as nr3,
      SUM(nr4) as nr4,
      SUM(nr5) as nr5,
      SUM(nr6) as nr6
    from spiel
    left join spieler on spiel.spielerId = spieler.id
    group by spieler.name;
EOSQL

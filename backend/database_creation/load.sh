#!/bin/bash
DB_HOST="192.168.1.77"
DB_USER="root"
mysql -u "$DB_USER" -h "$DB_HOST" -p < ddl.sql
mysql -u "$DB_USER" -h "$DB_HOST" -p < procedures.sql
mysql -u "$DB_USER" -h "$DB_HOST" -p < triggers.sql
mysql -u "$DB_USER" -h "$DB_HOST" -p < users.sql
mysql -u "$DB_USER" -h "$DB_HOST" -p < inserts.sql

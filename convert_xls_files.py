import os
from django.core.management import setup_environ

import settings
import logging

setup_environ(settings)

import xlrd
from django.db import connection, transaction

logger = logging.getLogger(__name__)

date_columns = [ 'Date' ]
varchar_columns = [ 'Opposition', 'Player Surname', 'Player Forename', 'Team', 'Venue' ]
special_columns = date_columns + varchar_columns + [ "Player ID", "Team Id", "Opposition id" ]
varchar_column_indices = [0, 2, 3, 4, 6, 8 ]
MAX_INDEXES_ALLOWED = 64

def fill_table(sheet, columns, name):
    cursor = connection.cursor()
    column_sql = """date, player_id, player_surname, player_forename, team, team_id, opposition, opposition_id, venue, """
    column_sql += ', '.join(columns)

    for row in range(sheet.nrows):
        if row == 0:
            continue

        row_values = [ ]
        count = 0
        for value in sheet.row_values(row):
            if count in varchar_column_indices:
                row_values.append("%s" % ('"' + value.encode('utf-8') + '"'))
            else:
                row_values.append(str(int(value)).encode('utf-8'))
            count += 1

        values_sql = ','.join(row_values)

        sql = 'INSERT INTO %s (%s) VALUES (%s);' % (str(name), str(column_sql), str(values_sql))
        # print sql

        cursor.execute(sql)
        transaction.commit_unless_managed()

def create_table(sheet):
    name = sheet.name     # Table name

    # The first row has the column names we want
    row_values = sheet.row_values(0)
    count = 0

    create_columns_sql = """date DATETIME, player_surname VARCHAR(30), player_forename VARCHAR(30),
                            team VARCHAR(50), opposition VARCHAR(50),
                            player_id INT, team_id INT, opposition_id INT, venue VARCHAR(30),
                            """

    create_indexes_sql = """INDEX (date), INDEX (player_surname), INDEX (player_forename),
                            INDEX (team), INDEX (opposition), INDEX (player_id), INDEX (team_id),
                            INDEX (opposition_id), INDEX (venue),
                         """
    index_count = 10

    columns = []
    for c in row_values:
        if c in special_columns:
            count += 1
            continue

        c = c.replace(' ', '_').replace('-', '_').lower()

        create_columns_sql += c + " " + "INT"
        columns.append(c)
        
        if index_count < MAX_INDEXES_ALLOWED:
            create_indexes_sql += " INDEX (" + c + ")"
            if index_count < MAX_INDEXES_ALLOWED-1:
                create_indexes_sql += ", "
            index_count += 1
        
        if count != sheet.ncols-1:
            create_columns_sql += ", "

        count += 1

    
    sql = 'CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, %s, %s ) ENGINE=innodb;' % (name, create_columns_sql, create_indexes_sql)
    print sql

    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        print ("Successfully created table: %s" % name)
    except Exception as e:
        print ("Failed to create table: %s, %s" % (name, e))

    fill_table(sheet, columns, name)

    print "Done."

def main():
    workbook = xlrd.open_workbook('../../mcfc_data/data.xls')
    sheets = workbook.sheets()
    for sheet in sheets:
        create_table(sheet)

if __name__ == "__main__":
    main()

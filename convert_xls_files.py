import os
from django.core.management import setup_environ

import settings
import logging

setup_environ(settings)

import xlrd
from django.db import connection, models

logger = logging.getLogger(__name__)

date_columns = [ 'Date' ]
varchar_columns = [ 'Opposition', 'Player Surname', 'Player Forename', 'Team', 'Venue' ]
special_columns = date_columns + varchar_columns + [ "Player ID", "Team Id", "Opposition id" ]
varchar_column_indices = [0, 2, 3, 4, 6, 8 ]

def create_table(sheet):
    name = sheet.name     # Table name

    # The first row has the column names we want
    row_values = sheet.row_values(0)

    column_map = {}
    for column in row_values:
        if column in varchar_columns:
            column_map[column] = "VARCHAR(20)"
            print column_map
        elif column in date_columns:
            column_map[column] = "DATETIME"
        else:
            column_map[column] = "INT"

    create_columns_sql = ''
    count = 0
    columns = []

    create_columns_sql = """date DATETIME, player_surname VARCHAR(20), player_forename VARCHAR(20),
                            team VARCHAR(20), opposition VARCHAR(20),
                            player_id INT, team_id INT, opposition_id INT,
                            """

    for k,v in sorted(column_map.iteritems()):
        if k in special_columns:
            count += 1
            continue

        k = k.replace(' ', '_').replace('-', '_').lower()

        columns.append(k)
        create_columns_sql += k + " " + v
        if count != sheet.ncols-1:
            create_columns_sql += ", "

        count += 1
    
    sql = 'CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, %s) ENGINE=innodb;' % (name, create_columns_sql)
    print sql
    cursor = connection.cursor()

    try:
        cursor.execute(sql)
        print ("Successfully created table: %s" % name)
    except Exception as e:
        print ("Failed to create table: %s, %s" % (name, e))


    column_sql = ', '.join(columns)

    for row in range(sheet.nrows):
        if row == 0:
            continue

#        row_values = [ ]
#        count = 0
#        for value in sheet.row_values(row):
#            if count in varchar_column_indices:
#                row_values.append("%s" % ("'" + str(value) + "'"))
#            else:
#                row_values.append(str(value))
#            count += 1
#
#        values_sql = ','.join(row_values)
#
#        sql = 'INSERT INTO %s (%s) VALUES (%s);' % (name, column_sql, values_sql)
#        print sql
#        cursor.execute(sql)

def main():
    workbook = xlrd.open_workbook('../../mcfc_data/data.xls')
    sheets = workbook.sheets()
    for sheet in sheets:
        create_table(sheet)

if __name__ == "__main__":
    main()

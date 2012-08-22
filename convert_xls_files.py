import os
from django.core.management import setup_environ

import settings
import logging

setup_environ(settings)

import xlrd
from django.db import connection, models

logger = logging.getLogger(__name__)

def create_table(sheet):
    name = sheet.name     # Table name

    # The first row has the column names we want
    row_values = sheet.row_values(0)

    column_map = {}
    for column in row_values:
       column_map[column] = "INT"

    create_columns_sql = ''
    count = 0
    for k,v in column_map.iteritems():
        k = k.replace(' ', '_').lower()
        create_columns_sql += k + " " + v
        if count != sheet.ncols-1:
            create_columns_sql += ", "

        count += 1

    sql = 'CREATE TABLE %s ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, %s) type=innodb;' % (name, create_columns_sql)
    logger.info(sql)
    cursor = connection.cursor()
    try:
        cursor.execute(sql)
        print ("Successfully created table: %s" % name)
    except Exception as e:
        print ("Failed to create table: %s, %s" % (name, e))

def main():
    workbook = xlrd.open_workbook('../../mcfc_data/data.xls')
    sheets = workbook.sheets()
    for sheet in sheets:
        create_table(sheet)

if __name__ == "__main__":
    main()

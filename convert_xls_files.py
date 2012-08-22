import os
from django.core.management import setup_environ

import settings

setup_environ(settings)

import xlrd
from django.db import connection, models


workbook = xlrd.open_workbook('../../mcfc_data/data.xls')
sheets = workbook.sheets()
for sheet in sheets:
    name = sheet.name     # Table name

    for row_num in range(sheet.nrows):
        values = sheet.row_values(row_num) 

        if row_num == 0:
            column_map = {}
            for column in sheet.row_values(row_num):
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
        print sql
        cursor = connection.cursor()
        # cursor.execute(sql)

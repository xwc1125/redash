import cStringIO
import csv
import xlsxwriter
from redash.utils import json_loads, UnicodeWriter
from redash.query_runner import (TYPE_BOOLEAN, TYPE_DATE, TYPE_DATETIME)


def serialize_query_result_to_csv(query_result):
    s = cStringIO.StringIO()

    query_data = json_loads(query_result.data)

    fieldnames = []
    bool_columns = []
    date_columns = []
    datetime_columns = []

    for col in query_data['columns']:
        fieldnames.append(col['name'])
        if col['type'] == TYPE_BOOLEAN:
            bool_columns.append(col['name'])
        
        if col['type'] == TYPE_DATE:
            date_columns.append(col['name'])

        if col['type'] == TYPE_DATETIME:
            datetime_columns.append(col['name'])

    writer = csv.DictWriter(s, extrasaction="ignore", fieldnames=[col['name'] for col in query_data['columns']])
    writer.writer = UnicodeWriter(s)
    writer.writeheader()
    for row in query_data['rows']:

        for col in bool_columns:
            if col in row:
                if row[col] == True:
                    row[col] = "true"
                elif row[col] == False:
                    row[col] = "false"

        writer.writerow(row)

    return s.getvalue()


def serialize_query_result_to_xlsx(query_result):
    s = cStringIO.StringIO()

    query_data = json_loads(query_result.data)
    book = xlsxwriter.Workbook(s, {'constant_memory': True})
    sheet = book.add_worksheet("result")

    column_names = []
    for (c, col) in enumerate(query_data['columns']):
        sheet.write(0, c, col['name'])
        column_names.append(col['name'])

    for (r, row) in enumerate(query_data['rows']):
        for (c, name) in enumerate(column_names):
            v = row.get(name)
            if isinstance(v, list) or isinstance(v, dict):
                v = str(v).encode('utf-8')
            sheet.write(r + 1, c, v)

    book.close()

    return s.getvalue()
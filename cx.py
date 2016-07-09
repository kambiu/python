import cx_Oracle

def rows_as_dicts(cursor):
    """ returns cx_Oracle rows as dicts """
    colnames = [i[0] for i in cursor.description]
    for row in cursor:
        yield dict(zip(colnames, row))

conn_string = 'bwu/97319937@127.0.0.1/XE' # <username>/<password>@<ip>/<SID>
con = cx_Oracle.connect(conn_string)
print "Connect to Oracle Database v." + con.version


cur = con.cursor()
cur.execute('select * from product order by ID')

for row in rows_as_dicts(cur):
    print row
    print row["ID"]
    print row["REMARKS"]

# for row in cur:
#     print row_result

# for row_result in cur:
#     print row_result

    # for sub_column in row_result:
    #     print sub_column


cur.close()
con.close()

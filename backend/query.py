from decimal import Decimal
import pymysql

def connection_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="universitas_lks"
    )
    
def run_query(sql):
    conn = connection_db()
    cursor = conn.cursor()
    cursor.execute(sql)

    columns = [col[0] for col in cursor.description]
    result = []

    for row in cursor.fetchall():
        row_dict = {}

        for col, value in zip(columns, row):
            # convert Decimal ke float
            if isinstance(value, Decimal):
                value = float(value)

            row_dict[col] = value

        result.append(row_dict)

    cursor.close()
    conn.close()

    return result

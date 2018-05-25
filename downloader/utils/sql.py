import psycopg2


class Hyp3_Archive_Sql:
    def __init__(self, connection_string, check_granules_sql):
        self.connection_string = connection_string
        self.check_granules_sql = check_granules_sql
        self.get_connection()

    def get_connection(self):
        self.archive_connection = psycopg2.connect(self.connection_string)

    def is_granule_in_hyp3(self, product):
        exists = do_sql(self.archive_connection,
                        self.check_granules_sql,
                        {"name": product})
        return len(exists)


def do_sql(db_conn, sql, vals=None):
    cur = db_conn.cursor()
    cur.execute(sql, vals) if vals else cur.execute(sql)
    try:
        res = cur.fetchall()
    except (BaseException, Exception, KeyboardInterrupt):
        cur.close()
        return ""

    cur.close()
    return res

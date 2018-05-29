class Sql:
    def __init__(self, options):
        self.options = options

    def do_sql(self, db_conn, sql, vals=None):
        cur = db_conn.cursor()
        cur.execute(sql, vals) if vals else cur.execute(sql)

        try:
            res = cur.fetchall()
        except Exception:
            return
        else:
            return res
        finally:
            db_conn.commit()
            cur.close()

    def do_multiple_updates(self, db_conn, true_false, sql, products):
        cur = db_conn.cursor()
        for product in range(len(products)):
            vals = {'true_false': true_false,
                    'granule': products[product][0]}
            cur.execute(sql, vals)
        cur.close()

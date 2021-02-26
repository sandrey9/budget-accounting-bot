import os
import psycopg2
from urllib.parse import urlparse

postgres_dsn = os.getenv('POSTGRES_DSN')
p = urlparse(postgres_dsn)
con = psycopg2.connect(
    database=p.path.replace('/', ''),
    user=p.username,
    password=p.password,
    host=p.hostname,
    port=p.port
)


def add_outcome_category(name, chat_id):
    cur = con.cursor()
    cur.execute("INSERT INTO outcome_category (name, chat_id) VALUES (%s, %s);", (name, chat_id,))
    con.commit()
    print("Record inserted successfully")
    cur.close()


def delete_outcome_category(outcome_id):
    cur = con.cursor()
    cur.execute("UPDATE outcome_category SET is_deleted = TRUE WHERE id = %s AND is_default = FALSE RETURNING id;",
                (outcome_id,))
    con.commit()
    argument = cur.fetchall()
    print("Record inserted successfully")
    cur.close()
    return argument


def select_outcome_category(chat_id):
    cur = con.cursor()
    cur.execute(
        "SELECT name, id from outcome_category WHERE chat_id = %s AND is_deleted IS FALSE OR is_default = TRUE",
        (chat_id,))
    argument = cur.fetchall()
    con.commit()
    print("Record inserted successfully")
    cur.close()
    return argument


def add_income(amount, chat_id, username):
    cur = con.cursor()
    cur.execute("INSERT INTO income (amount, chat_id, username) VALUES (%s, %s, %s);", (amount, chat_id, username,))
    con.commit()
    print("Record inserted successfully")
    cur.close()


def add_outcome(chat_id, category_id, amount):
    cur = con.cursor()
    cur.execute("INSERT INTO outcome (chat_id, category_id, amount) VALUES (%s, %s, %s);",
                (chat_id, category_id, amount,))
    con.commit()
    print("Record inserted successfully")
    cur.close()


def get_report_json(created_at_from, created_at_to, chat_id):
    cur = con.cursor()
    cur.execute("""
    SELECT json_build_object('incomes', income, 'incomes_total_amount', incomes_total_amount, 'outcome', outcome,
                         'outcome_total_amount', outcome_total_amount)
FROM (
         SELECT (
                    SELECT json_agg(base)
                    FROM (
                             SELECT sum(inc.amount)               user_amount,
                                    inc.username                  username,
                                    concat(
                                            round(
                                                        100 * sum(inc.amount) /
                                                        (
                                                            SELECT sum(amount)
                                                            FROM income
                                                            WHERE chat_id IN (%s)
                                                              AND created_at >= %s
                                                              AND created_at <= %s
                                                        )), '%%') percentage
                             FROM income inc
                             WHERE inc.chat_id = %s
                               AND inc.created_at >= %s
                               AND inc.created_at <= %s
                             GROUP BY inc.username
                         ) base
                )
                    income,
                (
                    SELECT sum(amount)
                    FROM income
                    WHERE chat_id IN (%s)
                      AND created_at >= %s
                      AND created_at <= %s
                )   incomes_total_amount,
                (
                    SELECT json_agg(base)
                    FROM (
                             SELECT sum(o.amount)                 type_amount,
                                    oc.name                       type_name,
                                    concat(
                                            round(
                                                        100 * sum(o.amount) /
                                                        (
                                                            SELECT sum(amount)
                                                            FROM outcome
                                                            WHERE chat_id IN (%s)
                                                              AND created_at >= %s
                                                              AND created_at <= %s
                                                        )), '%%') percentage
                             FROM outcome o
                                      LEFT JOIN outcome_category oc on o.category_id = oc.id
                             WHERE o.chat_id = %s
                               AND o.created_at >= %s
                               AND o.created_at <= %s
                             GROUP BY oc.name
                         ) base
                )   outcome,
                (
                    SELECT sum(amount)
                    FROM outcome
                    WHERE chat_id IN (%s)
                      AND created_at >= %s
                      AND created_at <= %s
                )   outcome_total_amount
     ) a
    """, (chat_id, created_at_from, created_at_to, chat_id, created_at_from, created_at_to, chat_id, created_at_from,
          created_at_to, chat_id, created_at_from, created_at_to, chat_id, created_at_from, created_at_to, chat_id,
          created_at_from,
          created_at_to,))
    argument = cur.fetchall()
    con.commit()
    print("Record inserted successfully")
    cur.close()
    return argument[0][0]

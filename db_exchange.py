import sqlite3
from datetime import date
conn = sqlite3.connect(r'family_budget.db', check_same_thread=False)

cur = conn.cursor()

def create_table():
    cur.execute("""CREATE TABLE IF NOT EXISTS family_members
                (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT,
    spent INTEGER
);
    """)
    cur.execute("""CREATE TABLE IF NOT EXISTS temp_expenses
                (
    id INTEGER PRIMARY KEY,
    name TEXT,
    date TEXT,
    spent INTEGER
);
                """)
    cur.execute("""CREATE TABLE IF NOT EXISTS payment_dates
                (id INTEGER PRIMARY KEY,
                date TEXT)""")
    
    conn.commit()

def commit_expenses(name, inp):
    sql_main = "INSERT INTO family_members (name, date, spent) values(?, ?, ?)"
    sql_temp = "INSERT INTO temp_expenses (name, date, spent) values(?, ?, ?)"
    data = [
        (name, date.today(), inp)
    ]
    cur.executemany(sql_main, data)
    cur.executemany(sql_temp, data)
    conn.commit()


def sum_print_detalisation():
    try:
        sql = "SELECT SUM(spent) FROM temp_expenses"
        cur.execute(sql)
        records = cur.fetchall()
        res = [j for i in records for j in i]
        asc_desc = ["ASC", "DESC"]
        date_list = []
        for i in asc_desc:
            cur.execute(f"SELECT date FROM temp_expenses ORDER BY id {i} LIMIT 1")
            date_list.append(cur.fetchall())
        sum = '{0:,}'.format(res[0]).replace(',', ' ')
        date_f = [j for i in date_list[0] for j in i]
        date_l = [j for i in date_list[1] for j in i]
        save_dates(date.today())
        cur.execute(f"SELECT SUM(spent) FROM temp_expenses WHERE name = 'NAME1'")
        sum_list_alex = cur.fetchall()
        cur.execute(f"SELECT SUM(spent) FROM temp_expenses WHERE name = 'NAME2'")
        sum_list_yana = cur.fetchall()
        l1 = [str(j) for i in sum_list_alex for j in i]
        l2 = [str(j) for i in sum_list_yana for j in i]
        delete_table = "DELETE FROM temp_expenses"
        cur.execute(delete_table)   
        conn.commit()
        mess = f"""За расчетный период с {' '.join(date_f)} по {' '.join(date_l)} было потрачено:\n{sum} рублей.
        \nТраты по членам семьи: \n NAME1 {' '.join(l1)} рублей.\n NAME2 {' '.join(l2)} рублей."""
        alex_det = [j for i in sum_list_alex for j in i]
        yana_det = [j for i in sum_list_yana for j in i]
        total = (alex_det[0] + yana_det[0])/2 
        al_det = total - alex_det[0]
        yan_det = total - yana_det[0]
        if al_det<0:
            return f'{mess}\n\nName2 надо доплатить Алексею {yan_det} рублей.'
        if yan_det<0:
            return f'{mess}\n\nName1 надо доплатить Яне {al_det} рублей.'
    except Exception as e:
        return "Что-то сломалось :("


def save_dates(date):
    inp_date = date
    sql = "INSERT INTO payment_dates (date) values (?)"
    data = [(inp_date)]
    cur.execute(sql, data)
    conn.commit()


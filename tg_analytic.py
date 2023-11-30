import sqlite3 as sq
import datetime
import csv
import logging

logger3 = logging.getLogger(__name__)
logger3.setLevel(logging.INFO)
handler3 = logging.FileHandler(f"{__name__}.log")
formatter3 = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")

handler3.setFormatter(formatter3)
logger3.addHandler(handler3)

logger3.info(f'DB created for module {__name__}...')


def db_start():
    global db, cursor
    db = sq.connect('tganal.db')
    db.row_factory = sq.Row
    cur = db.cursor()
    if db:
        logger3.info(f'DataBases conected for module {__name__}...')
    cur.execute("CREATE TABLE IF NOT EXISTS analytic(user_id TEXT, data DATE, tg_message TEXT, descript TEXT, user_name TEXT)")
    db.commit()
    cur.close()

def db_add(userid, message, u_name):
    cur = db.cursor()
    mes_desc = ''
    data = datetime.datetime.today().strftime("%Y-%m-%d")
    if '/' in message:
        mes_desc = 'commands'
    else:
        mes_desc = 'sityname'
    cur.execute("INSERT INTO analytic VALUES(?, ?, ? ,?, ?)", (userid, data, message, mes_desc, u_name))
    db.commit()
    cur.close()
    logger3.info(f'{userid} used the {mes_desc} ...')

def csv_to_db():
    cur = db.cursor()
    with open('data.csv', encoding='UTF-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            cur.execute("INSERT INTO analytic VALUES(?, ?, ?, ?, ?)", (row['id'], row['data'], row['command'], row['desc'], row['user']))
            db.commit()
    
    cur.close()
    logger3.info(f'Data export from csv to database completed...')

def exp_db_txt():
    cur = db.cursor()
    with open('db_old.csv', 'a', newline="", encoding='UTF-8') as fil:
        wr = csv.writer(fil, delimiter=',')
        for result in cur.execute('SELECT user_id, data, tg_message, descript, user_name FROM analytic').fetchall():
            wr.writerow([result['user_id'], result['data'], result['tg_message'], result['descript'], result['user_name']])
        fil.close()
    cur.close()
    logger3.info(f'Data export from database to file csv completed...')

def out_stat():
    cur = db.cursor()
    st1 = '<code>количество пользователей: </code>' + '<b>' + str(cur.execute("SELECT COUNT(DISTINCT user_id) FROM analytic").fetchall()[0][0]) + '</b>'
    st2 = '<code>количество использований: </code>' + '<b>' + str(cur.execute("SELECT COUNT(*) FROM analytic").fetchall()[0][0]) + '</b>'
    st3 = '<code>использовано команд:      </code>' + '<b>' + str(cur.execute("SELECT COUNT(descript) FROM analytic WHERE descript = 'commands'").fetchall()[0][0]) + '</b>'
    st4 = '<code>запросов погоды:          </code>' + '<b>' + str(cur.execute("SELECT COUNT(descript) FROM analytic WHERE descript = 'sityname'").fetchall()[0][0]) + '</b>'
    statistika = f'<b>Общая статистика</b>\n{st1}\n{st2}\n{st3}\n{st4}'
    cur.close()
    logger3.info(f'General bot statistics generated...')
    return statistika

def user_stat():
    cur = db.cursor()
    txtsql = '<b>Активность пользователей:</b> ' + '\n'
    iduser = ''
    nnum = 0
    for ret in cur.execute("SELECT user_id, MAX(data), COUNT(tg_message) FROM analytic GROUP BY user_id").fetchall():
        if len(ret[0]) < 10:
            iduser = ret[0] + ' '
        else:
            iduser = ret[0]
        nnum += 1
        txtsql += f'<code>{str(nnum).ljust(4)} {iduser} {ret[1]} {str(ret[2]).rjust(4)}</code>\n'
    cur.close()
    logger3.info(f'User activity statistics generated...')
    return txtsql

def user_xname():
    cur = db.cursor()
    txtsql = '<b>Запросы пользователей: </b>' + '\n'
    nnum = 0
    for ret in cur.execute("SELECT user_name, MAX(data), COUNT(tg_message) FROM analytic GROUP BY user_name").fetchall():
        nnum += 1

        if len(str(nnum)) == 1:
            num = str(nnum) + '_'
        else:
            num = str(nnum)

        txtsql += f'<code>{str(num).ljust(3)} {ret[0]}, {ret[1]}, {str(ret[2]).rjust(4)}</code>\n'
    cur.close()
    logger3.info(f'Advanced user statistics generated...')
    return txtsql
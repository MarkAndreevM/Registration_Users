import sqlite3 as sq

from create_bot import bot

def sql_start():
    global base, cur
    base = sq.connect('registration_user.db')

    if base:
        print('Data base connected OK!')
    else:
        raise Exception('Ошибка подключения к базе данных')

    cur = base.cursor()
    base.execute('CREATE TABLE IF NOT EXISTS show_data(user_id TEXT, img TEXT, name TEXT, age TEXT, skills TEXT, phone INT(10))')
    base.commit()

async def sql_add_command(state):
    async with state.proxy() as data:
        cur.execute('INSERT INTO show_data VALUES (?,?,?,?,?,?)', tuple(data.values()))
        base.commit()

        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write(f"\n\n'Добавлен новый пользователь' \n\n"
                       f"Имя - {data.get('name')}\n"
                       f"Возраст - {data.get('age')}\n"
                       f"Навыки - {data.get('skills')}\n"
                       f"Номер телефона - {data.get('phone')}\n")





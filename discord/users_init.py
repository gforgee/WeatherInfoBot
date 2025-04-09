import os

users = {}


def init_users():
    try:
        for x in range(0, 3):
            dc_id = os.getenv(f'USER_ID{x}')
            if dc_id:  # Check if dc_id is not None
                users[dc_id] = ['Krakow']
            else:
                print(f'USER_ID{x} nie posiada wartosci')
        return users
    except Exception as e:
        print(f'[Error] users_init.py -> init_users() ->  {e}')


def dodaj_miasto(user_id: str, city='Krakow'):
    try:
        if city not in users[user_id][0]:
            users[user_id].append(city)
        elif user_id not in users:
            return f'{user_id} nie jest w slowniku'
        else:
            return f'[Error]{user_id} posiada już takie miasto {city}'
        return users
    except Exception as e:
        print(f'[Error] users_init.py -> dodaj_miasto() ->  {e}')

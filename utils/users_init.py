import os

users_dict = {}


def init_users():
    try:
        for key, value in os.environ.items():
            if key.startswith('USER_ID'): # Check if dc_id is not None
                users_dict[int(value)] = {'cities': [''], 'counter': 0, 'tasks': None}
        return users_dict
    except Exception as e:
        print(f'[Error] /utils ->  users_init.py -> init_users() ->  {e}')


def add_city(user_id: int, city='Krakow'):
    try:
        if city not in users_dict[user_id]['cities']:
            users_dict[user_id]['cities'].append(city)
        elif user_id not in users_dict:
            return f'{user_id} is not in dict'
        else:
            return f'[Error] /utils -> users_init.py -> add_city() -> {user_id} does have this {city} in dict'
        return users_dict
    except Exception as e:
        print(f'[Error] /utils -> users_init.py -> add_city() ->  {e}')

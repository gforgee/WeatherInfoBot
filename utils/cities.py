from utils.dateprinter import print_date

date = print_date()


def str_city_format(cities: str) -> list:
    try:
        city_list = cities.split(',')
        city_list = [city.strip().capitalize() for city in city_list]
        return city_list
    except Exception as e:
        print(f'({date}) [[Error] /utils -> cities.py -> str_city_format() ->  {e}')
        return []


def add_city(users_dict: dict, city_data, user_id: int):
    cities_list = str_city_format(city_data)
    if user_id not in users_dict:
        print(f'({date}) [Error] /utils -> users_init.py -> add_city() -> {user_id} is not in dict')
        return

    try:

        for city in cities_list:
            if city not in users_dict[user_id]['cities']:
                users_dict[user_id]['cities'].append(city)
            elif user_id not in users_dict:
                print(f'({date}) [Error] /utils -> users_init.py -> add_city() ->{user_id} is not in dict')
            elif city in users_dict[user_id]['cities']:
                print(
                    f'({date}) [Error] /utils -> users_init.py -> add_city() -> {user_id} already have this {city} in dict')
            else:
                print(f'({date}) [Error] /utils -> users_init.py -> add_city() -> else triggered in add_city')
        return users_dict
    except Exception as e:
        print(f'({date}) [[Error] /utils -> users_init.py -> add_city() ->  {e}')

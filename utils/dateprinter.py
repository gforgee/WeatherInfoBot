from datetime import datetime


def print_date():  # function to help printing date in main
    return datetime.now().strftime('%A %d.%m at %H:%M:%S')

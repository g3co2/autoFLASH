from gspread import Client, Spreadsheet, Worksheet, service_account, service_account_from_dict

from typing import List
from typing import Iterator

import re
from time import sleep
import os


LEVEL_TITLES = ['Базовый', 'Средний', 'Хард']
borders_type = {
    "style": "SOLID"
}
colours = [
    (182, 215, 168),
    (255, 229, 153),
    (234, 153, 153)
]


def client_init_json() -> Client:
    """Создание клиента для работы с Google Sheets."""
    return service_account_from_dict(eval(os.getenv('GOOGLE_APPLICATION_CREDENTIALS')))


def get_table_by_id(client: Client, table_url: str) -> Spreadsheet:
    """Получение таблицы из Google Sheets по ID таблицы."""
    return client.open_by_key(table_url)


def get_worksheet(sheet_title: str) -> Worksheet:
    """Создает сессию и возвращает объект листа на таблице"""
    client = client_init_json()
    table = get_table_by_id(client, os.getenv('GOOGLE_TABLE_ID'))

    worksheet = table.worksheet(title=sheet_title)
    return worksheet


def get_column_name(num: int):
    alphabet_length = ord('Z') - ord('A') + 1
    name = ''
    while num > 0:
        num -= 1
        name += chr(ord('A') + num % alphabet_length)
        num //= alphabet_length

    return name[::-1]


def write(title: str, deadline: str, totals: List[str], q_students: int, grades: Iterator[str]) -> None:
    """Записывает в табличку в последние столбцы инфу по домашке."""

    print(title, deadline, totals)

    worksheet = get_worksheet(os.getenv('YOUR_GOOGLE_SHEET_TITLE'))
    columns = [get_column_name(worksheet.col_count + i) for i in range(1, len(totals) + 1)]
    worksheet.add_cols(len(totals))

    worksheet.format(f'{columns[0]}', {
        "borders": {
            "left": borders_type
        }
    })

    worksheet.format(f'{columns[-1]}', {
        "borders": {
            "right": borders_type
        }
    })

    worksheet.update_acell(f'{columns[0]}1', title)
    worksheet.merge_cells(f'{columns[0]}1:{columns[-1]}2')
    worksheet.merge_cells(f'{columns[0]}4:{columns[-1]}4')
    worksheet.update_acell(f'{columns[0]}4', deadline)
    worksheet.format(f'{columns[0]}1:{columns[-1]}2', {
        "backgroundColor": {
            "red": 180 / 255,
            "green": 167 / 255,
            "blue": 214 / 255
        },
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "BOTTOM",
        "textFormat": {
            "fontSize": 10,
            "bold": True
        },
        "borders": {
            "right": borders_type,
            "left": borders_type,
            "bottom": borders_type
        }
    })

    for i, (colour, title, mark) in enumerate(zip(colours, LEVEL_TITLES, totals)):
        worksheet.update_acell(f'{columns[i]}3', mark)
        worksheet.update_acell(f'{columns[i]}5', title)
        worksheet.merge_cells(f'{columns[i]}5:{columns[i]}6')

        borders = {
            "bottom": borders_type
        }
        if i == 0:
            borders.update({"left": borders_type})
        if i == len(totals) - 1:
            borders.update({"right": borders_type})

        worksheet.format(f'{columns[i]}5:{columns[i]}6', {
            "backgroundColor": {
                "red": colour[0] / 255,
                "green": colour[1] / 255,
                "blue": colour[2] / 255
            },
            "horizontalAlignment": "CENTER",
            "verticalAlignment": "BOTTOM",
            "textFormat": {
                "fontSize": 8
            },
            "borders": borders
        })

    delay = 10
    for row in range(7, q_students + 7):
        for col in columns:
            worksheet.update_acell(f'{col}{row}', next(grades))

        delay -= 1
        if delay == 0:
            sleep(30)
            delay = 10


def get_last_deadline() -> str:
    worksheet = get_worksheet(os.getenv('YOUR_GOOGLE_SHEET_TITLE'))
    last_num = worksheet.col_count
    while True:
        try:
            date = worksheet.get(f'{get_column_name(last_num)}4')[0][0]
            if re.match(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$", date):
                return date
        except Exception as error:
            last_num -= 1
            print('from to_table.get_last_deadline skipped:', error)
            continue

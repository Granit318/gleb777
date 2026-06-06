import json
import re
from datetime import datetime

from django.utils import timezone

DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{2}:\d{2}$')
MAX_NAME_LENGTH = 50


def parse_upload_date(date_value: str) -> datetime:
    parsed = datetime.strptime(date_value, '%Y-%m-%d_%H:%M')
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed)
    return parsed


def validate_json_upload(content: str) -> tuple[list[dict], list[str]]:
    errors: list[str] = []

    try:
        data = json.loads(content)
    except json.JSONDecodeError as exc:
        return [], [f'Некорректный JSON: {exc.msg}']

    if not isinstance(data, list):
        return [], ['Файл должен содержать JSON-массив.']

    valid_items: list[dict] = []

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f'Элемент {index}: ожидается объект.')
            continue

        if 'name' not in item:
            errors.append(f'Элемент {index}: отсутствует ключ "name".')
            continue

        if 'date' not in item:
            errors.append(f'Элемент {index}: отсутствует ключ "date".')
            continue

        name = item['name']
        if not isinstance(name, str):
            errors.append(f'Элемент {index}: "name" должен быть строкой.')
            continue

        if len(name) >= MAX_NAME_LENGTH:
            errors.append(
                f'Элемент {index}: длина "name" должна быть меньше {MAX_NAME_LENGTH} символов.'
            )
            continue

        date_value = item['date']
        if not isinstance(date_value, str):
            errors.append(f'Элемент {index}: "date" должен быть строкой.')
            continue

        if not DATE_PATTERN.match(date_value):
            errors.append(
                f'Элемент {index}: "date" должен быть в формате YYYY-MM-DD_HH:mm.'
            )
            continue

        try:
            parsed_date = parse_upload_date(date_value)
        except ValueError:
            errors.append(
                f'Элемент {index}: "date" содержит некорректную дату или время.'
            )
            continue

        valid_items.append({'name': name, 'date': parsed_date})

    return valid_items, errors

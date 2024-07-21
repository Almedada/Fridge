from datetime import datetime, timedelta
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

goods = {
    'Фабрика №2: яйца': [
        {'amount': Decimal('2'), 'expiration_date': datetime.strptime('2024-07-19', DATE_FORMAT).date()},
        {'amount': Decimal('3'), 'expiration_date': datetime.strptime('2024-07-21', DATE_FORMAT).date()}
    ],
    'Яйца Фабрики №1': [
        {'amount': Decimal('1'), 'expiration_date': datetime.strptime('2024-07-23', DATE_FORMAT).date()}
    ],
    'макароны': [
        {'amount': Decimal('100'), 'expiration_date': None}
    ]
}


def add(items, title, amount, expiration_date=None):
    if title not in items:
        items[title] = []
    expiration_date = datetime.strptime(expiration_date, DATE_FORMAT).date() if expiration_date else expiration_date
    items[title].append({'amount': amount, 'expiration_date': expiration_date})


def add_by_note(items, note):
    parts = note.split(' ')
    if len(parts) > 1 and len(parts[-1].split('-')) == 3:
        expiration_date = parts[-1]
        good_amount = Decimal(parts[-2])
        title = ' '.join(parts[:-2])
    else:
        expiration_date = None
        good_amount = Decimal(parts[-1])
        title = ' '.join(parts[:-1])

    add(items, title, good_amount, expiration_date)
    print(items)


def find(items, needle):
    result = []
    needle = needle.lower()
    for item in items:
        if needle in item.lower():
            result.append(item)
    return result


def amount(items, needle):
    found_items = find(items, needle)
    total_amount = Decimal('0')
    if not found_items:
        return total_amount
    for found_item in found_items:
        for entry in items[found_item]:
            total_amount += entry['amount']
    return total_amount


def expire(items, in_advance_days=0):
    current_day = datetime.now().date()
    target_date = current_day + timedelta(days=in_advance_days)

    result = []

    for item, entries in items.items():
        total_amount = Decimal('0')
        for entry in entries:
            expiration_date = entry['expiration_date']
            if expiration_date:
                # Проверяем, если срок годности истёк или истечёт в течение указанного количества дней
                if expiration_date <= target_date:
                    total_amount += entry['amount']

        if total_amount > 0:
            result.append((item, total_amount))

    return result


#print(expire(goods, in_advance_days=2))  # Вывод результата в виде списка
#print(amount(goods, 'макароны'))  # Сумма количества для продукта
# add_by_note(goods, 'Макароны 1.5')  # Добавление нового продукта

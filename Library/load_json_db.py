import json
import sys
import os

sys.path.append(os.path.join('..'))
from Library.tables import Publisher, Book, Shop, Stock, Sale


def load_json_db(session):
    with open('Sample_db/tests_data.json', 'r') as fd:
        data_base = json.load(fd)
    for el in data_base:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[el.get('model')]
        table_id = {f"{list(model.__dict__.keys())[2]}": el.get('pk')}
        session.add(model(**table_id, **el.get('fields')))
    try:
        session.commit()
        print('Данные успешно загружены.')
    except:
        print('Данные уже существуют в базе.')
    return

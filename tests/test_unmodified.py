import csv as oldcsv
from io import StringIO

from defusedcsv import csv


def test_read():
    f = StringIO('Spam Spam Spam Spam Spam |Baked Beans|\nSpam |Lovely Spam| |Wonderful Spam|')
    spamreader = csv.reader(f, delimiter=' ', quotechar='|')
    assert list(spamreader) == [
        ['Spam', 'Spam', 'Spam', 'Spam', 'Spam', 'Baked Beans'],
        ['Spam', 'Lovely Spam', 'Wonderful Spam']
    ]


def test_has_attributes():
    assert hasattr(csv, 'reader')
    assert hasattr(csv, 'register_dialect')
    assert hasattr(csv, 'unregister_dialect')
    assert hasattr(csv, 'get_dialect')
    assert hasattr(csv, 'list_dialects')
    assert hasattr(csv, 'field_size_limit')
    assert hasattr(csv, 'DictReader')
    assert hasattr(csv, 'DictWriter')
    assert hasattr(csv, 'Dialect')
    assert hasattr(csv, 'excel')
    assert hasattr(csv, 'excel_tab')
    assert hasattr(csv, 'unix_dialect')
    assert hasattr(csv, 'Sniffer')
    assert hasattr(csv, 'QUOTE_ALL')
    assert hasattr(csv, 'QUOTE_MINIMAL')
    assert hasattr(csv, 'QUOTE_NONNUMERIC')
    assert hasattr(csv, 'QUOTE_NONE')
    assert hasattr(csv, 'Error')
    assert hasattr(csv, 'writer')
    assert hasattr(csv, '__doc__')
    assert hasattr(csv, '__version__')


def test_dialect_registry():
    assert 'test' not in oldcsv.list_dialects()
    assert oldcsv.list_dialects() == csv.list_dialects()

    class TestD(csv.excel):
        delimiter = ';'

    csv.register_dialect('test', TestD)

    assert 'test' in oldcsv.list_dialects()
    assert oldcsv.list_dialects() == csv.list_dialects()

    assert oldcsv.get_dialect('test').delimiter == ';'
    assert csv.get_dialect('test').delimiter == ';'

    csv.unregister_dialect('test')
    assert 'test' not in oldcsv.list_dialects()
    assert oldcsv.list_dialects() == csv.list_dialects()

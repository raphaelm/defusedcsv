import pytest
from io import StringIO

from defusedcsv import csv


def test_writer():
    f = StringIO()
    spamwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['@SUM(1+1)*cmd|\' /C calc\'!A0 '])
    spamwriter.writerows([['Spam', 'Lovely Spam', 'Wonderful Spam'], ['A', 'B', '=3+4']])

    f.seek(0)
    assert f.read() == "Spam Spam Spam Spam Spam |'@SUM(1+1)*cmd\\||' /C calc'!A0 |\r\n" \
                       "Spam |Lovely Spam| |Wonderful Spam|\r\nA B '=3+4\r\n"

    assert spamwriter.dialect


def test_dictwriter():
    f = StringIO()
    fieldnames = ['first_name', 'last_name']
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': '@SUM(1+1)*cmd|\' /C calc\'!A0 '})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

    f.seek(0)
    assert f.read() == "first_name,last_name\r\nBaked,Beans\r\n" \
                       "Lovely,'@SUM(1+1)*cmd\\|' /C calc'!A0 \r\nWonderful,Spam\r\n"


def test_writer_fail():
    f = StringIO()
    spamwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    with pytest.raises(csv.Error):
        spamwriter.writerow(None)

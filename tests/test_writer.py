from io import StringIO

from defusedcsv import csv

from unittest import TestCase


class WriterTests(TestCase):
    def test_writer(self):
        f = StringIO()
        spamwriter = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Spam'] * 5 + ['@SUM(1+1)*cmd|\' /C calc\'!A0 '])
        spamwriter.writerows([['Spam', 'Lovely Spam', 'Wonderful Spam'], ['A', 'B', '=3+4']])

        f.seek(0)
        assert f.read() == "Spam Spam Spam Spam Spam |'@SUM(1+1)*cmd\\||' /C calc'!A0 |\r\n" \
                           "Spam |Lovely Spam| |Wonderful Spam|\r\nA B '=3+4\r\n"

        assert spamwriter.dialect


    def test_asserting_writer(self):
        f = StringIO()
        spamwriter = csv.writer(f, assert_injection=True, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        self.assertRaises(csv.Error, spamwriter.writerow, ['Spam'] * 5 + ['@SUM(1+1)*cmd|\' /C calc\'!A0 '])
        self.assertRaises(csv.Error, spamwriter.writerows, [['Spam', 'Lovely Spam', 'Wonderful Spam'], ['A', 'B', '=3+4']])


class DictWriterTests(TestCase):
    def test_dictwriter(self):
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

    def test_asserting_dictwriter(self):
        f = StringIO()
        fieldnames = ['first_name', 'last_name']
        writer = csv.DictWriter(f, assert_injection=True, fieldnames=fieldnames)

        writer.writeheader()
        self.assertRaises(csv.Error, writer.writerow, {'first_name': 'Lovely', 'last_name': '@SUM(1+1)*cmd|\' /C calc\'!A0 '})

import re
from csv import (
    QUOTE_ALL, QUOTE_MINIMAL, QUOTE_NONE, QUOTE_NONNUMERIC, Dialect,
    DictReader, DictWriter as BaseDictWriter, Error, Sniffer, excel, excel_tab,
    field_size_limit, get_dialect, list_dialects, reader, register_dialect,
    unix_dialect, unregister_dialect, writer as basewriter,
)

__all__ = ["QUOTE_MINIMAL", "QUOTE_ALL", "QUOTE_NONNUMERIC", "QUOTE_NONE",
           "Error", "Dialect", "excel", "excel_tab", "field_size_limit", "reader", "writer",
           "register_dialect", "get_dialect", "list_dialects", "Sniffer",
           "unregister_dialect", "DictReader", "DictWriter", "unix_dialect"]


def escape(payload, assert_injection=False):
    if payload is None:
        return ''

    payload = str(payload)
    if payload and payload[0] in ('@', '+', '-', '=', '|', '%') and not re.match("^-?[0-9,\\.]+$", payload):
        if assert_injection is True:
            raise Error('The payload which shall be written is dangerous (CSV injection).')
        payload = payload.replace("|", "\\|")
        payload = "'" + payload
    return payload


class ProxyWriter:
    def __init__(self, writer, assert_injection):
        self.writer = writer
        self.assert_injection = assert_injection

    def writerow(self, row):
        self.writer.writerow([escape(field, self.assert_injection) for field in row])

    def writerows(self, rows):
        self.writer.writerows([[escape(field, self.assert_injection) for field in row] for row in rows])

    def __getattr__(self, item):
        return getattr(self.writer, item)


def writer(csvfile, assert_injection=False, dialect='excel', **fmtparams):
    return ProxyWriter(basewriter(csvfile, dialect, **fmtparams), assert_injection)


class DictWriter(BaseDictWriter):
    def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                 dialect="excel", assert_injection=False, *args, **kwds):
        super().__init__(f, fieldnames, restval, extrasaction, dialect, *args, **kwds)
        self.writer = writer(f, assert_injection, dialect, **kwds)

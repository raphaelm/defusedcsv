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


def escape(payload):
    if payload is None:
        return ''

    payload = str(payload)
    if payload and payload[0] in ('@', '+', '-', '=', '|', '%'):
        payload = payload.replace("|", "\|")
        payload = "'" + payload
    return payload


class ProxyWriter:
    def __init__(self, writer):
        self.writer = writer

    def writerow(self, row):
        self.writer.writerow([escape(field) for field in row])

    def writerows(self, rows):
        self.writer.writerows([[escape(field) for field in row] for row in rows])

    def __getattr__(self, item):
        return getattr(self.writer, item)


def writer(csvfile, dialect='excel', **fmtparams):
    return ProxyWriter(basewriter(csvfile, dialect, **fmtparams))


class DictWriter(BaseDictWriter):
    def __init__(self, f, fieldnames, restval="", extrasaction="raise",
                 dialect="excel", *args, **kwds):
        super().__init__(f, fieldnames, restval, extrasaction, dialect, *args, **kwds)
        self.writer = writer(f, dialect, **kwds)

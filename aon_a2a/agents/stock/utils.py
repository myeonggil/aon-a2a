from numbers_parser import Document

from dataclasses import dataclass


@dataclass
class NumbersDocument:
    stock_code: str
    stock_item: str
    market_division: str


def load_numbers_file(path: str = "./code.numbers") -> list[NumbersDocument]:
    doc = Document(path)
    sheets = doc.sheets
    tables = sheets[0].tables
    # 종목코드(stock_code), 종목명(stock_item), 시장구분(market_division)
    rows = tables[0].rows()
    results = []
    for row in rows[1:]:
        stock_code, stock_item, market_division = (
            str(int(row[0].value)) if isinstance(row[0].value, float) else row[0].value,
            row[1].value,
            row[2].value
        )
        numbers_doc = NumbersDocument(
            stock_code=stock_code,
            stock_item=stock_item,
            market_division=market_division
        )
        results.append(numbers_doc)
    return results

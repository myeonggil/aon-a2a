from aon_a2a.agents.stock.models import NumbersDocument

from numbers_parser import Document

from dataclasses import dataclass


def load_numbers_file(path: str = "./code.numbers") -> list[NumbersDocument]:
    doc = Document(path)
    sheets = doc.sheets
    tables = sheets[0].tables
    # 종목코드(stock_code), 종목명(stock_name), 시장구분(market_division)
    rows = tables[0].rows()
    results = []
    for row in rows[1:]:
        stock_code, stock_name, market_division = (
            str(int(row[0].value)) if isinstance(row[0].value, float) else row[0].value,
            row[1].value,
            row[2].value
        )
        numbers_doc = NumbersDocument(
            stock_code=stock_code,
            stock_name=stock_name,
            market_division=market_division
        )
        results.append(numbers_doc)
    return results

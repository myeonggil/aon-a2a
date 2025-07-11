from typing import Optional

from aon_a2a.configs import config

from dataclasses import dataclass, field


@dataclass
class RequestHeader:
    content_type: str = None    #컨텐츠타입
    authorization: str = None    #접근토큰
    appkey: str = None    #앱키
    appsecret: str = None    #앱시크릿키
    personalseckey: Optional[str] = None    #고객식별키
    tr_id: str = None    #거래ID
    tr_cont: Optional[str] = None    #연속 거래 여부
    custtype: str = None   #고객 타입
    seq_no: Optional[str] = None    #일련번호
    mac_address: Optional[str] = None    #맥주소
    phone_number: Optional[str] = None    #핸드폰번호
    ip_addr: Optional[str] = None    #접속 단말 공인 IP
    hashkey: Optional[str] = None    #해쉬키
    gt_uid: Optional[str] = None    #Global UID

@dataclass
class RequestQueryParam:
    FID_COND_MRKT_DIV_CODE: str = None    #조건 시장 분류 코드
    FID_INPUT_ISCD: str = None    #입력 종목코드


@dataclass
class StockInfo:
    stock_event: str = None
    stock_code: int = 0

@dataclass
class Stock:
    stock_name: str = None
    stock_info: StockInfo = None



from numbers_parser import Document
doc = Document("./code.numbers")
sheets = doc.sheets
tables = sheets[0].tables
rows = tables[0].rows()
stock_name = rows[1][1].value
stock_code = int(rows[1][0].value)
stock_event = rows[1][2].value

stock_info = StockInfo(stock_event=stock_event, stock_code=stock_code)
stock = Stock(stock_name=stock_name, stock_info=stock_info)
print(stock)

from typing import Optional
from dataclasses import dataclass


@dataclass
class RequestHeader:
    content_type: str = "application/json"    #컨텐츠타입
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

    def to_dict(self):
        return {
            "content-type": self.content_type,
            "authorization": f"Bearer {self.authorization}",
            "appkey": self.appkey,
            "appsecret": self.appsecret,
            "personalseckey": self.personalseckey,
            "tr_id": self.tr_id,
            "tr_cont": self.tr_cont,
            "custtype": self.custtype,
            "seq_no": self.seq_no,
            "mac_address": self.mac_address,
            "phone_number": self.phone_number,
            "ip_addr": self.ip_addr,
            "hashkey": self.hashkey,
            "gt_uid": self.gt_uid
        }

@dataclass
class RequestQueryParam:
    FID_COND_MRKT_DIV_CODE: str = None    #조건 시장 분류 코드
    FID_INPUT_ISCD: str = None    #입력 종목코드


@dataclass
class StockInfo:
    market_division: str = None # ex) KOSDAQ, KOSPI
    stock_code: int = 0 # Number of specific stock

@dataclass
class Stock:
    stock_item: str = None  # Name of stock
    stock_info: StockInfo = None
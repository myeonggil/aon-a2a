from typing import Optional

from aon_a2a.configs import config

from dataclasses import dataclass


@dataclass
class RequestHeader:
    content_type: str    #컨텐츠타입
    authorization: str    #접근토큰
    appkey: str    #앱키
    appsecret: str    #앱시크릿키
    personalseckey: Optional[str] = None    #고객식별키
    tr_id: str    #거래ID
    tr_cont: Optional[str] = None    #연속 거래 여부
    custtype: str    #고객 타입
    seq_no: Optional[str] = None    #일련번호
    mac_address: Optional[str] = None    #맥주소
    phone_number: Optional[str] = None    #핸드폰번호
    ip_addr: Optional[str] = None    #접속 단말 공인 IP
    hashkey: Optional[str] = None    #해쉬키
    gt_uid: Optional[str] = None    #Global UID

@dataclass
class RequestQueryParam:
    FID_COND_MRKT_DIV_CODE: str    #조건 시장 분류 코드
    FID_INPUT_ISCD: str    #입력 종목코드

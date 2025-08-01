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
class ResponseHeader:
    content_type: str    #컨텐츠타입
    tr_id: str    #거래ID
    tr_cont: Optional[str] = None    #연속 거래 여부
    gt_uid: Optional[str] = None    #Global UID


@dataclass
class ResponseBodyoutput:
    iscd_stat_cls_code: str    #종목 상태 구분 코드
    marg_rate: str    #증거금 비율
    rprs_mrkt_kor_name: str    #대표 시장 한글 명
    new_hgpr_lwpr_cls_code: str    #신 고가 저가 구분 코드
    bstp_kor_isnm: str    #업종 한글 종목명
    temp_stop_yn: str    #임시 정지 여부
    oprc_rang_cont_yn: str    #시가 범위 연장 여부
    clpr_rang_cont_yn: str    #종가 범위 연장 여부
    crdt_able_yn: str    #신용 가능 여부
    grmn_rate_cls_code: str    #보증금 비율 구분 코드
    elw_pblc_yn: str    #ELW 발행 여부
    stck_prpr: str    #주식 현재가
    prdy_vrss: str    #전일 대비
    prdy_vrss_sign: str    #전일 대비 부호
    prdy_ctrt: str    #전일 대비율
    acml_tr_pbmn: str    #누적 거래 대금
    acml_vol: str    #누적 거래량
    prdy_vrss_vol_rate: str    #전일 대비 거래량 비율
    stck_oprc: str    #주식 시가2
    stck_hgpr: str    #주식 최고가
    stck_lwpr: str    #주식 최저가
    stck_mxpr: str    #주식 상한가
    stck_llam: str    #주식 하한가
    stck_sdpr: str    #주식 기준가
    wghn_avrg_stck_prc: str    #가중 평균 주식 가격
    hts_frgn_ehrt: str    #HTS 외국인 소진율
    frgn_ntby_qty: str    #외국인 순매수 수량
    pgtr_ntby_qty: str    #프로그램매매 순매수 수량
    pvt_scnd_dmrs_prc: str    #피벗 2차 디저항 가격
    pvt_frst_dmrs_prc: str    #피벗 1차 디저항 가격
    pvt_pont_val: str    #피벗 포인트 값
    pvt_frst_dmsp_prc: str    #피벗 1차 디지지 가격
    pvt_scnd_dmsp_prc: str    #피벗 2차 디지지 가격
    dmrs_val: str    #디저항 값
    dmsp_val: str    #디지지 값
    cpfn: str    #자본금
    rstc_wdth_prc: str    #제한 폭 가격
    stck_fcam: str    #주식 액면가
    stck_sspr: str    #주식 대용가
    aspr_unit: str    #호가단위
    hts_deal_qty_unit_val: str    #HTS 매매 수량 단위 값
    lstn_stcn: str    #상장 주수
    hts_avls: str    #HTS 시가총액
    per: str    #PER
    pbr: str    #PBR
    stac_month: str    #결산 월
    vol_tnrt: str    #거래량 회전율
    eps: str    #EPS
    bps: str    #BPS
    d250_hgpr: str    #250일 최고가
    d250_hgpr_date: str    #250일 최고가 일자
    d250_hgpr_vrss_prpr_rate: str    #250일 최고가 대비 현재가 비율
    d250_lwpr: str    #250일 최저가
    d250_lwpr_date: str    #250일 최저가 일자
    d250_lwpr_vrss_prpr_rate: str    #250일 최저가 대비 현재가 비율
    stck_dryy_hgpr: str    #주식 연중 최고가
    dryy_hgpr_vrss_prpr_rate: str    #연중 최고가 대비 현재가 비율
    dryy_hgpr_date: str    #연중 최고가 일자
    stck_dryy_lwpr: str    #주식 연중 최저가
    dryy_lwpr_vrss_prpr_rate: str    #연중 최저가 대비 현재가 비율
    dryy_lwpr_date: str    #연중 최저가 일자
    w52_hgpr: str    #52주일 최고가
    w52_hgpr_vrss_prpr_ctrt: str    #52주일 최고가 대비 현재가 대비
    w52_hgpr_date: str    #52주일 최고가 일자
    w52_lwpr: str    #52주일 최저가
    w52_lwpr_vrss_prpr_ctrt: str    #52주일 최저가 대비 현재가 대비
    w52_lwpr_date: str    #52주일 최저가 일자
    whol_loan_rmnd_rate: str    #전체 융자 잔고 비율
    ssts_yn: str    #공매도가능여부
    stck_shrn_iscd: str    #주식 단축 종목코드
    fcam_cnnm: str    #액면가 통화명
    cpfn_cnnm: str    #자본금 통화명
    apprch_rate: str    #접근도
    frgn_hldn_qty: str    #외국인 보유 수량
    vi_cls_code: str    #VI적용구분코드
    ovtm_vi_cls_code: str    #시간외단일가VI적용구분코드
    last_ssts_cntg_qty: str    #최종 공매도 체결 수량
    invt_caful_yn: str    #투자유의여부
    mrkt_warn_cls_code: str    #시장경고코드
    short_over_yn: str    #단기과열여부
    sltr_yn: str    #정리매매여부
    mang_issu_cls_code: str    #관리종목여부


@dataclass
class ResponseBody:
    rt_cd: str    #성공 실패 여부
    msg_cd: str    #응답코드
    msg1: str    #응답메세지
    output: ResponseBodyoutput    #응답상세


@dataclass
class StockInfo:
    stock_code: str # Number of specific stock
    stock_name: str  # Name of stock
    market_division: str # ex) KOSDAQ, KOSPI

    def to_dict(self):
        return {
            "stock_code": self.stock_code,
            "stock_name": self.stock_name,
            "market_division": self.market_division
        }


@dataclass
class RequestQueryParam:
    FID_COND_MRKT_DIV_CODE: str = None    #조건 시장 분류 코드
    FID_INPUT_ISCD: str = None    #입력 종목코드


@dataclass
class AssistantPrompt:
    market_trend = """
        {stock_name}의 최근 52주 최저가는 {low_price},
        최근 52주 최고가는 {high_price},
        현재가는 {now_price}으로 나타난다.
    """

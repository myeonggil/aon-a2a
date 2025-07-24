# KIS(Korea Investment) API

## API Doc
1. 인증(OAuth)
    - POST: oauth2/tokenP API 요청을 통해 access_token을 발급받는다
    - 발급받을 때마다 문자가 오며 1일의 유효기간이 있다
    - sqlite에 토큰을 저장하여 관리한다
2. 시세조회
    - GET: /uapi/domestic-stock/v1/quotations/inquire-price 

## workflow
- example: 삼성전자 주식에 관심이 있어서 투자를 하려고해 지난 몇달 동안 상한과 하한을 기록했던 때의 뉴스기사에 대해 분석하고 결과를 pdf형태로 만들어줘
- 삼성전자라는 주식 아이템에 대한 키워드를 추출해서 종목 코드를 얻는다
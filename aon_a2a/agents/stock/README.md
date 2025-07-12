# KIS(Korea Investment) API

## API Doc
1. 인증(OAuth)
    - POST: oauth2/tokenP API 요청을 통해 access_token을 발급받는다
    - 발급받을 때마다 문자가 오며 1일의 유효기간이 있다
    - sqlite에 토큰을 저장하여 관리한다
2. 시세조회
    - GET: /uapi/domestic-stock/v1/quotations/inquire-price 

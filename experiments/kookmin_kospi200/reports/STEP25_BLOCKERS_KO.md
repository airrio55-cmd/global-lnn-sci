# STEP2.5 남은 차단 항목

확인일2026-11-16 KST. B01만 완전 해소됐다. PARTIAL은 증거가 늘었다는 뜻이며 모델/HMM 실행 허가가 아니다.

| 항목 | 판정 | 해소된 부분 | 여전히 필요한 자료 |
|---|---|---|---|
| B01 | PASS | 공식 KRX3939세션·주말/휴장·임시휴일·session_id | 달력 gate 추가 요구 없음; 가격/공표는 별도 |
| B02 | PARTIAL | 45개 모두 실제 개장일이고 CSV에 없음 | 날짜별 공식 KOSPI200 종가·산출 근거. 공식 API/export 영수증, 수치/단위/수정 metadata |
| B03 | PARTIAL | 공식 정보상품·전송 절차 문서, 원본 해시 | 원본 실제 공급처·추출코드·지수 식별자·개정/다운로드 이력·t18:00 가용성·공식 가격 일치 대조 |
| B04 | PARTIAL | 공식2021~2025달력·early10개·DST16년64probe·특이휴장 | 공식2010~2020 전체 세션·earlyclose, 역사적 지수 종가 확정 규칙, 첨부 CSV 공급처별 latency/available_at 및 max_age |
| B05 | BLOCKED | 날짜·열·해시만 확인, 실시간 사용 차단 | 시장범위·현물/선물·금액/수량·단위·부호·잠정/확정·최초공표·개정·수집코드 |
| B06 | PARTIAL | 후보식9개3854행 수치 일치 | 실제 생성 코드·버전·입력 원천·PIT·수정 이력. 검증 전 기본 입력 제외 |
| B07 | PARTIAL | 저장torch2.10.0+cpu, 공식ncps1.0.1 소스/배포해시·τ/solver 정적검증 | 원본ncps/hmmlearn exact version·전체 환경lock·wiring/constraint metadata·dt 단위·권한있는 checkpoint. 호환성 실행은 STEP3 승인 후 |

B02/B03 가격 접근: KRX Marketplace JSON 조회는HTTP400 `LOGOUT`. 공식 API는 로그인·인증키·서비스 승인을 요구한다. 공공 조회의403·HTTP200 오류본문·PDF 대신HTML 반환도 source catalog에 실패/범위제한으로 기록했다. 네트워크 접근과 데이터 권한은 별개다. 다른 공급처 가격으로 빈칸을 채워 공식 검증을 대신하지 않았다.

대체 확인 경로:

- KRX [Open API 서비스](https://openapi.krx.co.kr/contents/OPP/INFO/service/OPPINFO004.cmd) 중 KOSPI 시리즈 일별시세정보를 승인된 계정으로 확보하거나, 공식 개별지수 시세 export를 제공받아 hash·조회조건·권한을 기록한다. 임의 로그인·개인정보 제출·키 신청은 수행하지 않았다.
- [KRX 휴장일 화면](https://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp)은 공개 조회로 확보됐으며, 가격조회가 실패했다는 이유로 달력까지 실패라고 쓰지 않았다.
- [Nasdaq 공식 달력](https://www.nasdaqtrader.com/Trader.aspx?id=Calendar)의 과거 원문/공식 공지 archive와 해당 CSV 공급처의 실제 게시·개정 이력이 필요하다. 현행17:16 지수 문서나 장 종료16시를 CSV available_at으로 대입하지 않는다.
- 외국인 A(제외)는 기존 F1/F2 범위에서 사전 명시할 수 있지만 다른 gate를 면제하지 않는다. B(이전 세션)는 공개시각 증빙 없이는 여전히 BLOCKED다. 결과에 따른 사후선택은 없다.

마지막2025년20세션은 종가 확보를 위해2026자료를 사용하는 대신 계속 unknown/평가 제외한다. 기존 원본을 수정하지 않고 검증된 보완가격이 생기면 별도 파일에만 추가한다. 현재 보완파일은0행이다.

모든 출처의 URL·조회시각·응답SHA-256·사용기준·한계는 `provenance/step25_source_catalog.json`, 달력은 `provenance/krx_calendar_provenance.json`에 있다. 출처가 확인되지 않은 원본 필드는 source_url=null/UNKNOWN을 유지한다. 근거 없는 값을 채워PASS로 바꾸지 않는다.

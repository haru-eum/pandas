# import streamlit as st
import pandas as pd
import numpy as np

trade = pd.read_csv('raw_trade_data.csv', encoding="cp949")
# print(trade.head())

# 1. hs_code, start = 85
print(trade.info())
cond_hs = trade['hs_code'].astype(str).str.startswith('85')

# 2. 미국과 베트남 in 국가명
cond_country = trade['국가명'].isin(['미국', '베트남'])

# 3. 수출금액이 0원인 데이터 제외
print(trade.head(10))
cond_value = trade['수출금액']>0

# 최종 결합 (1)
step1 = trade[cond_hs]
step2 = step1[cond_country]
step3 = step2[cond_value]
print(step3.head(10))

# 최종 결합 (2)
step3 = trade[cond_hs & cond_country & cond_value]
print(step3.head())

# 2번 문제 클렌징 및 정규화
# 1. 중량 컬럼 결측치 처리
print(trade.head(15))

hs_mean = trade.groupby('hs_code')['중량'].mean() #hs_code 그룹별로 묶어주고 중량 평균을 구했규나
print(hs_mean)

for hs in hs_mean.index: # .index -> value값만 가져오는 것
    # (1) 현재 순서의 hs_code에 해당하는 평균값 가져오기
    avg_val = hs_mean[hs]
    # (2) 원본 데이터에서 해당 hs이면서 중량이 비어있는 행만 찾기
    target = (trade['hs_code'] == hs) & (trade['중량'].isna())
    # (3) 해당되는 칸에만 평균값 대입
    trade.loc[target, '중량'] = avg_val

# trade.loc[trade['중량'].isna()]=0 평균 말고 그냥 0으로 채우기

# 2. import와 export를 수입 수출 한글로 바꾸기이
trade.loc[trade['수출입구분'] == 'Export', '수출입구분'] = '수출'
# trade['수출입구분'] == 'Export'의 행을 찾아서 그 행의 '수출입구분' 열 데이터를 바꿀게에
trade.loc[trade['수출입구분'] == 'Import', '수출입구분'] = '수입'

# 3. 수출금액 단위 변환 원 -> 백만달러 (금액/1470)/1000000
trade['수출금액_M.USD'] = (trade['수출금액']/1470)/1000000

# 4. 데이터 타입 확인
print('\n ---- [최종 데이터 확인] ----')
print(trade.dtypes)

print('\n ---- [클렌징 결과 샘플 확인] ----')
print(trade[['날짜', 'hs_code', '수출입구분', '수출금액_M.USD']].head(10))

# 최종 데이터 저장!!!
trade.to_csv('./cleaned_trade_data.csv', encoding='cp949', index=False)
print('과제 2 완료 cleaned_trade_data.csv이 저장되었습니다.')
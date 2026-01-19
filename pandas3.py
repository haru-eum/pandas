# 과제 2
import pandas as pd
import numpy as np

# encoding='cp949' 옵션을 추가합니다
bandoce = pd.read_csv("raw_trade_data.csv", encoding="cp949")

weight_error = bandoce[bandoce['중량'].isna()]
print(weight_error)

print(weight_error['hs_code'].value_counts())

list_error = list(weight_error['hs_code'].value_counts().index)
print(list_error)

mean_table = dict(bandoce.groupby('hs_code')['중량'].mean())
print(mean_table)


for code in list_error:
    # (1) 미리 만들어둔 사전(mean_table)에서 해당 코드의 평균값을 가져옵니다.
    mean_val = mean_table.get(code)
    
    # (2) 평균값이 존재하고(None이 아니고), 숫자인 경우(NaN이 아님)에만 실행
    if mean_val is not None and not np.isnan(mean_val):
        
        # (3) 조건 설정: '해당 코드'이면서 동시에 '중량이 비어있는' 행 찾기
        condition = (bandoce['hs_code'] == code) & bandoce['중량'].isna()
        
        # (4) 해당 조건에 맞는 곳에 평균값 대입
        bandoce.loc[condition, '중량'] = mean_val


# 결과 확인
print("\n[최종 결과 확인]")
print(bandoce.head())
# 결측치가 남았는지 확인 (0이 나와야 성공)
print("남은 결측치 수:", bandoce['중량'].isna().sum())

# 1. 'Import'라고 적힌 행을 찾아서 '수입'으로 변경
bandoce.loc[bandoce['수출입구분'] == 'Import', '수출입구분'] = '수입'

# 2. 'Export'라고 적힌 행을 찾아서 '수출'로 변경
bandoce.loc[bandoce['수출입구분'] == 'Export', '수출입구분'] = '수출'

# 1. 환율 변수 설정 (가독성을 위해)
exchange_rate = 1470

# 2. 계산식 적용 (백만 달러로 변환)
# 수식: (원화금액 / 환율) / 1,000,000
bandoce['수출금액_M_USD'] = (bandoce['수출금액'] / exchange_rate) / 1000000

# 3. 데이터 타입(dtypes) 확인
print("[데이터 타입 확인]")
print(bandoce.dtypes)

# 4. 결과 눈으로 확인 (새로 생긴 컬럼 확인)
print("\n[데이터 미리보기]")
print(bandoce[['수출금액', '수출금액_M_USD']].head())


    

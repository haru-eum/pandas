import pandas as pd
import numpy as np

# encoding='cp949' 옵션을 추가합니다
bandoce = pd.read_csv("raw_trade_data.csv", encoding="cp949")

hs_85 = bandoce[bandoce['hs_code'].astype(str).str.startswith('85')]

country_hs85 = hs_85[hs_85['국가명'].isin(['미국', '베트남'])]

erase_zero = country_hs85[country_hs85['수출금액'] != 0]
print(erase_zero.head(10))

import openpyxl

erase_zero.to_csv('./bandoce_info.csv', index = False)
print('파일 저장이 완료되었음')
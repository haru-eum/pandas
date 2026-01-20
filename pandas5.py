import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# trade = pd.read_csv('trade_performance.csv', encoding="cp949")
# country = pd.read_csv('country_master.csv', encoding="cp949")

try:
    # 데이터 가져오기
    df_perf = pd.read_csv('trade_performance.csv', encoding="cp949")
    df_master = pd.read_csv('country_master.csv', encoding="cp949")
except FileNotFoundError:
    print('경로 잘 설정할 것')
    exit()

# Step 1: 데이터 통합 (Merge)
# 두 파일을 ctry_code를 기준으로 병합하여, 실적 데이터에 국가명과 대륙 정보가 나타나도록 하세요.
df_total = pd.merge(df_perf, df_master, on= 'ctry_code', how='left')  # 엑셀의 vlookup이라는 함수와 같은 역할!
# on = 무엇을 기준으로 병합? how = 어떤 데이터에 보조 데이터를 병합할 건지. 원래 left가 디폴트
print(df_total.head(15))

# Step 2: 대륙별 성과 분석 (Aggregation)
# 병합된 데이터를 활용하여 대륙별 총 수출액과 총 수입액을 구하세요.
continent_stat = df_total.groupby('continent')[['export_val', 'import_val']].sum()
print(continent_stat)

# 어느 대륙과의 거래에서 가장 큰 무역수지(수출-수입) 흑자가 발생했는지 확인하세요.
# continent_stat에 새로운 열' 무역수지' 만들어 계산식 넣어주기
continent_stat['무역수지'] = continent_stat['export_val'] - continent_stat['import_val']
print('대륙별 무역 성과 요약')
print(continent_stat)

best_continent = continent_stat['무역수지'].idxmax()
# idxmax(): 가장 큰 수치의 라벨(첫번째 열) 가지고 들어와
print(f'분석 결과: {best_continent} 대륙과의 거래에서 가장 큰 무역 수지 흑자 발생')


# Step 3: FTA 효과 분석 (Groupby)
df_total['평균 수출 단가'] = df_total['export_val']/df_total['weight']

# FTA 체결 국가(fta_status == 'Y')와 미체결 국가(fta_status == 'N')의 **평균 수출 단가(수출금액/중량)**를 비교하세요.
fta_ans = df_total.groupby('fta_status')['평균 수출 단가'].mean()
#groupby('뭐로 그룹화')['어떤 결과를 보고 싶어']

print('\n FTA 여부에 따른 평균 수출 단가 비교')
print(fta_ans)

# FTA 체결이 수출 경쟁력에 기여하고 있는지 수치로 증명하세요.
if fta_ans['Y'] > fta_ans['N']: # 이거 딕셔너리 형태라서 이렇게 쓸 수 있는 거임
    print('단가가 너무 높음. FTA인데도 단가 높아서 수출 경쟁력이 안 좋은 듯..')
else:
    print('미체결국의 단가가 더 높음. 당연함.')

# Step 4: 품목별 집중도 분석 (Filtering)

# 특정 품목(hs_code) 중 수출 금액이 가장 큰 상위 2개 품목을 찾으세요.
top2_hs = df_total.groupby('hs_code')['export_val'].sum().nlargest(2).index.tolist()
# .nlargest(n) 큰 값 중에 n개 찾아와 ↔️ .nsmallest(n)
# .index.tolist() 딕셔너리 형태로 나오는 거를 value 값만 리스트 형태로 추출해줘
# 8541    35579943 ➡️ [8541, 8542]
# 8542    32125775
print(f'\n 수출 상위 2개 품목: {top2_hs}')


# 해당 품목들이 주로 어느 국가로 수출되고 있는지 분석하세요.
top2_df = df_total[df_total['hs_code'].isin(top2_hs)] 

country_focus = top2_df.groupby(['hs_code', 'ctry_name'])['export_val'].sum().reset_index()
# .reset_index() : 읽기 좋은 형태의 dataframe으로 읽어와라
print(country_focus)

# Step 5: 시각화 및 인사이트 도출 (Visualization)
# ---------------------------------------------------------
# [추가할 코드] 한글 폰트 설정 (Windows 기준)
plt.rc('font', family='Malgun Gothic')

# [추가할 코드] 마이너스(-) 기호가 깨지는 것 방지
plt.rc('axes', unicode_minus=False)
# ---------------------------------------------------------

df_total['ymd'] = pd.to_datetime(df_total['ymd'])
df_total['month'] = df_total['ymd'].dt.month # 월 별로 묶어라

# 월별 수출입 추이를 선 그래프로 시각화하세요.
monthly = df_total.groupby('month')[['export_val', 'import_val']].sum()
plt.figure(figsize=(12,6))
plt.plot(monthly.index, monthly['export_val'], label = '수출액', marker='o', linewidth=2)
# monthly.index 월로 묶은 거를 순서대로 가져오겠다
plt.plot(monthly.index, monthly['import_val'], label = '수입액', marker='s', linewidth=2)

plt.title('월별 수출입 실적 추이')
plt.xlabel('월(month)') # x축
plt.ylabel('금액') # y축
plt.show() # plt를 보여라



# 분석 결과를 바탕으로 "다음 분기에 마케팅을 집중해야 할 국가/대륙"을 1문장으로 제안하세요. 

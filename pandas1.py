# 엑셀 자료의 전처리 과정에서 꼭 필요한 판다스 라이브러리 불러오기
import pandas as pd
import numpy as np

dict_data = {"a": 1, "b": 2, "c": 3}
series_data = pd.Series(dict_data) # series : 열머리
print(type(series_data))
print(series_data)

list_data = ["2026-1-19", 3.14, "Hello", 100, True]
series_data = pd.Series(list_data)
print(type(series_data))
print(series_data)

dict_data = {"c0": [1,2,3], "c1": [4,5,6], "c2": [7,8,9], "c3": ["a", "b", "c"], "c4": [True, False, True]}
df = pd.DataFrame(dict_data)
print(type(df))
print(df) 

# pandas 데이터 내용 확인
# .columns : 컬럼 명 확인
# .head() : 상위 5개 행 확인 (괄호 안에 숫자 지정 가능)
# .tail() : 하위 5개 행 확인 (괄호 안에 숫자 지정 가능)
# .shape : (행, 열) 크기 확인
# .info() : 데이터에 대한 전반적인 정보 제공
# 행과열의 크기, 컬럼명, 컬럼별 결측치, 컬럼별 데이터 탕입 등
# .type() : 데이터 타입 확인

# 파일 불러오기
# 형식    읽기        쓰기
# csv    read_csv    to_csv
# excel  read_excel  to_excel
# json   read_json   to_json
# html   read_html   to_html
# sql    read_sql    to_sql

#./ 내 기준 하위 폴더로 이동
#../ 내 기준 지금 폴더 나가서 상위 폴더로 이동

titanic = pd.read_csv("Titanic-Dataset.csv")
print(titanic)
print(titanic.columns)
print(titanic.head())
print(titanic.tail(10))
print(titanic.shape)
print(titanic.info())

print(type(titanic))

# pandas에서 특정 열 선택하기
# 열 1개 선택 = series 객체 반환
# 데이터 프레임의 열 데이터 1개만 선택할 때의 2가지 방법
# 1) 대괄호 [] 안에 열 이름을 따옴표로 함께 입력
# 2) 점. 다음에 열 이름 입력

# 열 n개 선택 = DataFrame 객체로 바꾸어 반환

# 데이터 프레임의 열 데이터 n개를 선택할 때는 1가지 방법만 존재
# 이중대괄호[[]] 안에 열 이름을 따옴표로 함께 입력

# ☆ 만약에 열 1개를 데이터 프레임 객체로 추출하려면 [[]] 사용 가능

names = titanic["Name"]
print(names.head())
names = titanic.Name
print(names.head())
print(type(names))
print(names.shape)

tt = titanic[['Sex', 'Age']]
print(tt.head())
print(type(tt))
print(tt.shape)

# pandas에서 데이터 필터링
# 1. boolean 인덱싱 True 값을 지닌 행만 추출

# 2. .isin() 각각 요소가 데이터프레임 또는 시리즈에 존재하는지 파악하여 boolean 값으로 반환

# 3. .isna() 결측치 여부를 판단하여 boolean 값으로 반환

# 4. .notna() 결측치가 아닌지 여부를 판단하여 boolean 값으로 반환

print(tt['Age'] <= 26)

below26 = tt[tt['Age'] <= 26] # boolean 인덱싱, tt['Age'] <= 26을 필드명처럼 사용하여 True 값을 지닌 행만 추출
print(below26.head())

namja = tt[tt['Sex'] == 'male']
print(namja.head())

print(titanic.head())
rich = titanic['Pclass'].isin([1])
print(titanic[rich].head())
print(rich.head())

print(tt.head())
age2040 = tt[tt['Age'].isin(np.arange(20,41))] # 20~40세 사이의 승객 필터링, np.arange(20,41) : 20~40까지의 정수 배열 생성
print(age2040.head())

print(tt.head(7))
no_age = tt['Age'].isna()
print(no_age.head(7))

# 결측 값을 제거한 눌락되지 않은 값을 확인
# 행제거
print(tt.head(10))
erase_age = tt[tt['Age'].notna()]
print(erase_age.head(10))

# 결측치 제거
# .dropna(axis=0) == .dropna() : 결측치가 있는 행 전체 제거
# .dropna(axis=1) : 결측치가 있는 열 전체 제거
print(titanic.head(10))
print(titanic.dropna())

print(titanic.dropna(axis=1).head())

# pandas 이름과 인덱스로 특정 행과 열 선택
# .loc[] : 이름으로 행과 열 선택, 행이름 열이름    DataFrame객체.loc[행이름, 열이름]
# .iloc[] : 정수 인덱스로 행과 열 선택, 행번호 열번호    DataFrame객체.iloc[행번호, 열번호]

name35 = titanic.loc[titanic['Age'] >= 35, ['Name', 'Age']]
print(name35.head())
print()
a_name35 = name35.iloc[[1,2,3],0]
print(a_name35.head())
print()
name35.iloc[[1,2,3],0] = 'Anonymous'
print(name35.head())

# 판다스 데이터 통계
# .mean() : 평균
# .median() : 중앙값
# .describe() : 다양한 통계량 요약, mean, std, min, max, 25%, 50%, 75% 등
# .agg : 여러 개의 열에 다양한 함수 적용
# 모든 열에 여러 함수를 매핑: group.객체.agg([함수1, 함수2, ...])
# 특정 열에 여러 함수를 매핑: group.객체['열이름'].agg([함수1, 함수2, ...])
# 각 열마다 다른 함수를 매핑: group.객체.agg({'열이름1': 함수1, '열이름2': 함수2, ...})
# .groupby() : 특정 열을 기준으로 그룹화하여 통계량 산출
# .value_counts() : 값의 개수
print('--------평균 나이--------')
print(titanic['Age'].mean()) #타이타닉의 나이 필드값의 평균! 수치가 있는 필드에만 적용
print('--------나이 중앙값--------')
print(titanic['Age'].median()) #타이타닉의 나이 필드값의 중앙값! 수치가 있는 필드에만 적용
print('--------다양한 통계량 요약--------')
print(titanic.describe())
print('-------여러 열에 동일한 함수 적용-------')
print(titanic[['Age', 'Fare']].agg(['mean', 'std'])) # 함수에도 따옴표를 붙여야 함
print('-------열 별 사용자 집계-------')

agg_dict = {
    'Age': ['min', 'max', 'mean'],
    'Fare': ['median', 'sum']}
print(titanic.agg(agg_dict)) # 열 별로 다른 함수를 적용하여 집계

print('-----성별 기준으로 평균 나이 및 요금-----')
print(titanic.groupby('Sex')[['Age', 'Fare']].mean()) # 필드값이 여러개인 경우[[]]

print('-----객실 등급(Pclass)별 인원수-----')
print(titanic['Pclass'].value_counts()) # 필드값이 하나인 경우 []

print('-----성별 인원수-----')
print(titanic['Sex'].value_counts())

print('-----새로운 열 country 생성 "USA"-----')
titanic['Country']="USA" # 없는 열이면 생성, 있는 열이면 값 바꿈
print(titanic.head())

print('-----기존의 열을 계산해서 새로운 열 추가-----')
titanic['New_Age'] = titanic['Age'] + 10
print(titanic.head())

# 20세 미만이면 child, 아니면 adult
print('-----나이로 조건별 새로운 열 생성-----')
titanic['Status'] = 'adult'

titanic.loc[titanic['Age'] < 20, 'Status'] = 'child'

print(titanic.head(10))

# 데이터 프레임의 가장 마지막 인덱스 확인 후 행 추가
original_inde = len(titanic) # 숫자로 나옴!! 
print(original_inde)
print(titanic.head())
# 한 행만 추가할 때는 리스트 괜춘
titanic.loc[original_inde] = [892,1,1,'Eum', 'female',26,4,0,'PC123',58.99,'C123','s','KOR',36,'adult'] # 인덱스 번호 중요하기에 결측치 불가능
print(titanic.tail())

# 여러개 추가할 때는 데이터프레임이 괜춘
new_data = pd.DataFrame({
    'Name': ['배지수', '배똥수'],
    'Age': [30, 40],
    'Sex': ['female', 'female'],
    'Survived': [1,1]
}) # 키로 접근하기 때문에 순서 중요하지 않음
titanic1 = pd.concat([titanic, new_data])
print(titanic1.tail())
titanic2 = pd.concat([titanic, new_data], ignore_index=True) # 인덱스 번호 배정
print(titanic2.tail())

# titanic['Name'].str.startswith('Sa') # 문자열 데이터, Sa로 시작하는 이름만 가져오겠다
# titanic[ titanic["Age"].astype(str).str.startswith('2') ] # 숫자 데이터의 경우 문자열로 바꾸어야 함. 바깥에를 묶어줘야 필드값으로 가져오는 것임!!!
# titanic[ titanic["Age"].astype(str).str.startswith('^2') ] 중간 글자가 2인 경우

# 결과 도출한 것을 파일로 저장하고 싶다!
import openpyxl

titanic.to_csv('./titanic_info.csv', index = False) # 내가 있는 경로에 저장할 경우, 파일명과 확장자만 잡아주면 됨.
titanic.to_excel('./titanic_info.xlsx', index = False)
print('파일 저장이 완료되었음')
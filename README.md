# MarkCloud_Search API

## Test Environment

- OS: macOS
- Python: 3.12.7

## Environment Setup

```
# Create Virtual Env

$ python3 -m venv venv
$ source venv/bin/activate  # macOS/Linux
```

```
# Download packages

$ pip install -r requirements.txt
```

```
# Execute ElasticSearch

$ docker-compose up -d
```

```
# Indexing Data into Elasticsearch

$ python bulk_upload.py
```

## API Document

### 🔍 POST /api/search

상표 데이터에 대해 키워드 기반 검색 및 다양한 조건 필터링이 가능합니다.

### 📥 Request Body

```
{
  "keyword": "맥스",                              // [Required] string
  "registerStatus": "등록",                       // [Optional] string
  "asignProductMainCodeList": ["30"],            // [Optional] array of string
  "registrationDateFrom": "YYYY-MM-DD",          // [Optional] date format
  "registrationDateTo": "YYYY-MM-DD",            // [Optional] date format
  "page": 1,                                     // [Optional] integer
  "size": 10                                     // [Optional] integer
}
```

### 📤 Response Body

```
{
  "total": 158,
  "page": 1,
  "size": 10,
  "results": [
    {
      "id": "abc123",
      "score": 14.2,
      "source": {
        "productName": "맥스커피",
        "applicationNumber": "4020123456789",
        "registerStatus": "등록",
        ... 생략 ...
      }
    },
    ... 생략 ...
  ]
}
```

## Feature Overview

본 API는 Elasticsearch 기반 상표 검색 시스템입니다. 주요 기능은 다음과 같습니다:

- 한글/영문 상표명을 포함한 키워드 기반 검색
- 등록 상태, 상품 분류 코드, 등록일 범위에 따른 정교한 필터링 지원
- Ngram 기반 한글 형태소 유사 검색 + Fuzzy 검색 결합
- 결과 정렬 및 페이지네이션 기반 응답 반환

## Trade-off

데이터 검색 시스템을 구축함에 있어 다음 조건을 만족할 수 있는 검색 엔진을 평가했습니다:

- 러닝 커브가 낮고 빠르게 구축 가능할 것
  - Elasticsearch는 풍부한 문서, 커뮤니티, Python 공식 클라이언트를 제공하여 빠른 학습과 구현이 가능
- FastAPI + Python에서의 클라이언트 지원 여부
  - elasticsearch-py 및 elasticsearch-async 클라이언트가 공식 제공되며, FastAPI 비동기 구조와의 통합이 쉬움
- 데이터 변경 주기
  - 상표 데이터는 신규 등록 및 상태 변경이 자주 발생함 → 실시간 색인이 필수
  - Elasticsearch는 near real-time 색인을 지원해 최신 데이터를 검색 가능하게 함
- 정교한 필터링 및 정렬, 페이징 기능 필요
  - bool query, range, terms, sort, from/size 등 풍부한 Query DSL 지원
- SQL처럼 정렬, 조건 필터링이 자유롭고 확장 가능
  - 실제로도 빠른 성능과 낮은 응답 지연, 높은 유연성을 제공하고 있음

## 문제 해결 과정에서 고민했던 점

- “간호사” vs “간호샤” vs “간효사” 등의 입력에 대해 얼마나 유사한 결과를 보여줄지에 대한 고민
  - 해결책: ngram_analyzer + fuzzy 검색을 함께 사용
- JSON 내 등록일, 등록번호가 리스트로 오는 문제 → bulk 삽입 전 정규화 처리
- FastAPI 비동기 환경에서 Elasticsearch 연결을 싱글턴으로 재사용하는 방식 구현 (on_shutdown에서 close())

## 개선하고 싶은 부분

- 실시간 색인을 위한 API 추가

  - 현재는 초기 일괄 색인을 통해 데이터가 Elasticsearch에 저장되며, 이후 데이터 추가 및 갱신은 반영되지 않는 구조입니다. 향후에는 신규 데이터를 등록/수정/삭제할 수 있는 API를 추가하여, 실시간 색인(near real-time indexing) 구조를 완성하고 싶습니다.

- 검색 결과 정렬 및 랭킹 개선
  - 현재는 Elasticsearch 기본 scoring에 의존하고 있어, 키워드 매칭만으로 랭킹이 정해지는 구조입니다. 사용자 관점에서 더 적절한 결과가 상위에 노출되도록, 사용자 피드백 기반 랭킹 개선을 적용하고 싶습니다.

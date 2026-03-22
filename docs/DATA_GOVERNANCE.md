# DATA_GOVERNANCE.md
## Infovail-IQ PoC1 — Data Governance Policy

> **Version**: 1.0.0 | **Date**: 2026-03-04 | **Author**: Suah Cheon, MD
>
> 이 문서는 Infovail-IQ PoC1에서 수집·처리·보관하는 데이터의 관리 정책을 기술합니다.
> 데이터 수집 착수 전 확정하고, 연구 진행에 따라 업데이트합니다.

---

## 1. 데이터 수집 정책

### 1.1 수집 범위

| 항목 | 내용 |
|------|------|
| **플랫폼** | 네이버(Naver) |
| **채널** | 뉴스 댓글, 블로그 게시물 *(cafearticle 제외 — Naver Search API 날짜 필드 미제공)* |
| **수집 방법** | Naver Search API (공식 API) |
| **수집 기간** | 2026-02-07 ~ 2026-03-21 (6주) |
| **검색 키워드** | `PROMPT_REGISTRY.md` Section: 키워드 목록 참조 |
| **수집 대상** | 공개(public) 게시물만 수집 |
| **제외 대상** | 비공개 게시물, 회원 전용 게시물, 접근 제한 콘텐츠 |

### 1.2 플랫폼 이용약관 준수

- Naver Search API 이용 정책 및 일일 호출 제한(rate limit) 준수
- 수집 간격: API 호출 간 최소 0.5초 딜레이 적용 (서버 과부하 방지)
- 수집된 원본 데이터를 제3자에게 재배포하지 않음
- 상업적 목적으로 사용하지 않음

### 1.3 수집 항목

수집되는 필드는 아래와 같습니다. 연구 목적에 필요한 최소한의 정보만 수집합니다.

| 필드명 | 설명 | PII 여부 |
|--------|------|----------|
| `post_id` | 게시물 고유 식별자 (내부 생성) | 없음 |
| `channel` | 채널 구분 (news_comment / cafe / blog) | 없음 |
| `content` | 게시물 본문 텍스트 | 간접 가능 |
| `author_hash` | 작성자 닉네임의 SHA-256 해시값 | 없음 (원본 닉네임 저장 안 함) |
| `published_at` | 게시 일시 (날짜 단위) | 없음 |
| `keyword` | 수집에 사용된 검색 키워드 | 없음 |
| `collected_at` | 수집 일시 | 없음 |

> **저장하지 않는 항목**: 원본 닉네임, URL, IP 주소, 이메일, 프로필 정보, 게시물 URL (역추적 방지)

---

## 2. 개인정보(PII) 비식별화 정책

### 2.1 비식별화 절차

수집 즉시(ingestion 단계) 아래 절차를 적용합니다.

**Step 1 — 닉네임 해시 처리**
```python
import hashlib

def hash_author(nickname: str) -> str:
    return hashlib.sha256(nickname.encode('utf-8')).hexdigest()
```
원본 닉네임은 메모리에만 존재하며 디스크에 저장하지 않습니다.

**Step 2 — 본문 텍스트 준정제**

본문에서 아래 패턴을 자동 마스킹 처리합니다 (`preprocessor.py` 적용):
- 전화번호 패턴: `[PHONE_REDACTED]`로 대체
- 이메일 주소: `[EMAIL_REDACTED]`로 대체
- 주민등록번호 패턴: `[ID_REDACTED]`로 대체

**Step 3 — 논문 인용 시 추가 익명화**

논문 또는 공개 보고서에 게시물 내용을 인용할 경우, 특정 개인을 식별할 수 있는 고유명사(특이한 닉네임, 지역명 등)를 `[익명]`으로 처리합니다. 원문의 의미를 훼손하지 않는 범위에서 적용합니다.

### 2.2 재식별 리스크 관리

- `author_hash`를 역산하여 원본 닉네임을 복원하려는 시도를 하지 않습니다
- 동일 해시가 여러 게시물에 걸쳐 나타나는 경우, 개인 행동 패턴 추적 목적으로 사용하지 않습니다
- 소규모 카페 게시물 등 맥락상 작성자를 특정할 수 있는 경우, 해당 게시물은 분석에서 제외하거나 추가 익명화를 적용합니다

---

## 3. 데이터 저장 및 접근 정책

### 3.1 저장 구조

```
data/                          # .gitignore 대상 — 전체 비공개
├── raw/                       # 수집 원본 (비식별화 전 임시)
│   └── [즉시 처리 후 삭제]
├── processed/                 # 비식별화 완료 데이터
│   ├── naver_posts.db         # SQLite DB (메인 저장소)
│   └── backups/               # 일일 백업
└── exports/                   # 분석 결과 내보내기
    ├── labeled/               # LLM 분류 결과
    └── gold_standard/         # 수동 코딩 결과 (100건)
```

### 3.2 SQLite DB 스키마

```sql
CREATE TABLE posts (
    post_id      TEXT PRIMARY KEY,
    channel      TEXT NOT NULL,         -- 'news_comment' | 'cafe' | 'blog'
    content      TEXT NOT NULL,
    author_hash  TEXT NOT NULL,         -- SHA-256 해시
    published_at DATE NOT NULL,
    keyword      TEXT,
    collected_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE labels (
    post_id       TEXT REFERENCES posts(post_id),
    label_type    TEXT NOT NULL,        -- 'llm' | 'manual'
    c1_confidence INTEGER,              -- 0 or 1
    c2_complacency INTEGER,
    c3_constraints INTEGER,
    c4_calculation INTEGER,
    c5_collective INTEGER,
    c6_compliance INTEGER,
    c7_conspiracy INTEGER,
    na_flag       INTEGER DEFAULT 0,
    labeled_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    labeler_id    TEXT                  -- 'llm_v1' | 'coder_A' | 'coder_B'
);
```

### 3.3 접근 권한

| 접근 주체 | 접근 가능 데이터 | 비고 |
|-----------|----------------|------|
| 연구자 (수아) | 전체 | 로컬 환경 |
| 공저자 | Gold Standard 100건 (익명화 후) | 수동 코딩 목적 |
| GitHub 공개 저장소 | 코드, 문서, 샘플 데이터만 | 원본 데이터 제외 |
| 외부 연구자 | 샘플 데이터만 (`generate_sample_data.py` 생성) | 재현 목적 |

### 3.4 저장 위치

- 로컬 저장소: 연구자 개인 컴퓨터 (암호화 디스크 권장)
- 클라우드 백업: 개인 클라우드 스토리지 (비공개 설정)
- GitHub: 코드 및 문서만 업로드. `data/` 디렉토리는 `.gitignore`에 포함

---

## 4. 데이터 보관 및 폐기 정책

### 4.1 보관 기간

| 데이터 유형 | 보관 기간 | 근거 |
|-------------|-----------|------|
| 비식별화 처리된 수집 데이터 | 논문 게재 후 3년 | 연구 재현 가능성 확보 |
| Gold Standard (수동 코딩 100건) | 논문 게재 후 5년 | 학술지 데이터 보관 요건 |
| 분석 결과 및 코드 | 무기한 (GitHub 공개) | 오픈사이언스 원칙 |
| 원본 수집 데이터 (비식별화 전 raw) | 비식별화 완료 즉시 삭제 | PII 최소 보유 원칙 |

### 4.2 폐기 절차

보관 기간 만료 시:
1. SQLite DB 파일 안전 삭제 (단순 삭제가 아닌 덮어쓰기 방식)
2. 클라우드 백업 삭제
3. 폐기 일시 및 방법을 이 문서에 기록

---

## 5. 데이터 공개 정책 (오픈사이언스)

### 5.1 공개 항목

GitHub 공개 저장소에 포함되는 항목:

| 항목 | 공개 형태 |
|------|----------|
| 수집 스크립트 (`naver_client.py`) | 전체 공개 |
| 전처리 스크립트 (`preprocessor.py`) | 전체 공개 |
| 분류 프롬프트 (`PROMPT_REGISTRY.md`) | 전체 공개 |
| 분석 코드 (시계열, 공동출현) | 전체 공개 |
| 7C_CODEBOOK.md | 전체 공개 |
| 샘플 데이터 (`generate_sample_data.py` 생성) | 전체 공개 |

### 5.2 비공개 항목

| 항목 | 비공개 사유 |
|------|------------|
| 원본 수집 데이터 (`data/`) | 개인정보 보호, 플랫폼 이용약관 |
| LLM API 키 (`.env`) | 보안 |
| 로컬 LLM 모델 파일 (`.gguf`) | 용량 및 라이선스 |

### 5.3 샘플 데이터 생성

재현 가능성을 위해 `scripts/generate_sample_data.py`는 실제 데이터와 동일한 스키마를 가진 합성 샘플 데이터를 생성합니다. 실제 게시물 내용을 포함하지 않습니다.

---

## 6. 보안 정책

- API 키 및 인증 정보는 `.env` 파일에 저장하며, `.gitignore`에 포함
- `.env.example`에 키 이름만 공개 (값 미포함)
- 로컬 SQLite DB 파일은 암호화 디스크 또는 암호화 아카이브에 보관 권장
- 공저자와 데이터 공유 시 암호화 채널(이메일 암호화 또는 보안 파일 전송) 사용

---

## 7. 버전 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|-----------|
| 1.0.0 | 2026-03-04 | 초안 작성 |

---

*이 문서는 데이터 수집 착수 전 확정하고, 실제 수집 과정에서 발생하는 변경사항을 반영하여 업데이트합니다.*

# ClickStream Insight

**실시간 사용자 행동 로그 분석 시스템 구축 프로젝트**

Kafka, Logstash, Elasticsearch, Kibana를 사용하여 유저의 클릭/노출/구매 이벤트 로그를 실시간으로 수집, 저장, 시각화하는 데이터 파이프라인을 구성한 1인 프로젝트입니다.

---

## 주요 목표

- Kafka를 사용해 실시간 로그 전송 환경 구성
- Logstash로 Kafka의 로그를 수신하여 Elasticsearch에 저장
- Kibana를 통해 로그 데이터 분석 및 시각화
- 로그 유형을 다양화하여 유저 행동 패턴 추적
- (확장 예정) Spark를 통해 클릭 수 집계 처리 및 시각화

---

## 시스템 아키텍처

```
[Python 로그 생성기]
↓
[Kafka]
↓
[Logstash]
↓
[Elasticsearch]
↓
[Kibana]
```

---

## 사용 기술

| 분야 | 기술 |
|------|------|
| 메시지 브로커 | Apache Kafka |
| 로그 수집 | Logstash |
| 데이터 저장 | Elasticsearch |
| 시각화 | Kibana |
| 로그 생성기 | Python (`kafka-python`) |
| 컨테이너 환경 | Docker Compose |

## 구성 디렉터리
```
project/
├── docker-compose.yml
├── logstash/
│ └── pipeline/
│ └── logstash.conf
├── producer/
│ ├── venv/ (gitignore)
│ ├── log_producer.py
│ └── requirements.txt
└── README.md
```

---

## 📝 로그 이벤트 유형

| 로그 종류 | 설명 | Kafka Topic | Elasticsearch Index |
|-----------|------|-------------|----------------------|
| 클릭 로그 | 사용자가 상품을 클릭 | `click-log` | `click-logs` |
| 노출 로그 | 상품이 화면에 노출됨 | `expose-log` | `expose-logs` |
| 구매 로그 | 상품을 구매함 | `purchase-log` | `purchase-logs` |

---

## ⚙️ 실행 방법

### 1. Docker Compose 실행

```bash
docker-compose up -d
cd producer
source venv/bin/activate  # or use your own virtualenv
python log_producer.py
```

### 2.  Kibana 접속 및 로그 확인
Kibana: http://localhost:5601

### 3. 결과 예시 (Kibana Discover)
```json
{
  "userId": "user_17",
  "productId": "product_3",
  "timestamp": "2025-08-06T14:25:12.123Z"
}
```

Stack Management → Index Pattern 생성:
click-logs*, expose-logs*, purchase-logs*
Discover에서 실시간 로그 확인



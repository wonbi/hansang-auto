# 제철이 가득한 한상 — 인스타 / 쓰레드 자동 발행

`hansang.market` 계정에 매일 정해진 시각에 글과 영상을 올린다.
사람은 사진과 상품 정보만 넘기고, 나머지는 깃허브가 돈다.

- 스토어 · https://smartstore.naver.com/nice__food
- 인스타 · https://www.instagram.com/hansang.market/
- 쓰레드 · https://www.threads.com/@hansang.market

월 비용 0원. 깃허브 Actions(공개 저장소 무료), jsDelivr CDN, Meta API 모두 무료다.

---

## 폴더

```
hansang-auto/
├── post.py              발행기. 오늘 날짜·지난 시각 행을 찾아 올린다
├── generate_content.py  facts.json + threads.json → reels.json, queue.csv
├── make_reel.py         reels.json → 1080x1920 MP4
├── refresh_token.py     60일 만료 토큰 갱신
├── facts.json           (아직 없음) 릴스 자막·캡션 재료
├── threads.json         (아직 없음) 쓰레드 글
├── queue.csv            발행 큐 — 실제로 이걸 보고 올린다
├── assets/              원본 상품 사진
├── media/               발행용 사진·영상 (CDN 공개 경로)
└── .github/workflows/
    ├── daily-post.yml       20분마다 + push 시 즉시
    ├── weekly-content.yml   콘텐츠 자동 생성 (지금은 수동 실행만)
    └── monthly-refresh.yml  매달 1일 토큰 갱신
```

## 발행 시각

| 시각 | 채널 | 내용 |
|---|---|---|
| 12:00 | 쓰레드 | 글 (사진 첨부 가능) |
| 18:00 | 인스타 | 릴스 |
| 20:00 | 쓰레드 | 글 |

`queue.csv` 의 `time` 열이 실제 시각을 정한다. 위 값은 생성기 기본값일 뿐이다.

## 필요한 Secrets

저장소 Settings → Secrets and variables → Actions

| 이름 | 값 |
|---|---|
| `THREADS_USER_ID` | `me` |
| `THREADS_TOKEN` | 쓰레드 장기 토큰 |
| `IG_USER_ID` | `17841422371276671` |
| `IG_TOKEN` | 인스타 장기 토큰 |
| `GH_PAT` | 토큰 자동 갱신용 (Secrets 읽기·쓰기 권한) |

토큰은 60일 만료. `monthly-refresh.yml` 이 매달 1일 갱신하지만 `GH_PAT` 이 있어야 동작한다.

## 알아둘 것

**미디어는 공개 URL이어야 한다.** 메타 서버가 우리 주소를 직접 열어서 가져간다.
그래서 이 저장소는 공개다. `raw.githubusercontent.com` 은 `application/octet-stream` 으로
내보내서 메타가 거부하므로 `cdn.jsdelivr.net` 을 쓴다. 파일당 20MB 제한.

**깃허브 예약 실행은 2~5시간씩 밀린다.** 그래서 `post.py --watch` 가 한 번 깨어나면
그날 남은 시각까지 대기하다가 제때 올린다. 한 건 올릴 때마다 결과를 바로 기록해서
중간에 끊겨도 같은 글이 두 번 올라가지 않는다.

**이미지는 JPG만.** 인스타가 PNG·WebP를 거부한다. 파일명은 영문·숫자·하이픈만.

**영상은** MP4 / H.264 / 9:16 / 20MB 이하.

## 링크 성과

- 쓰레드 — 본문 링크가 클릭된다. 상품별로 다른 주소를 넣으면 상품별 반응이 보인다
- 인스타 — 캡션 링크는 클릭이 안 된다. 프로필 링크만 유효

인스타 쪽은 날짜 대조 + 네이버 애널리틱스 유입 경로로 본다.

## 지금 상태

엔진만 올라가 있다. `facts.json` 과 `threads.json` 이 없어서 아직 아무것도 발행하지 않는다.
상품 사진과 정보가 들어오면 콘텐츠를 만들고 `weekly-content.yml` 의 schedule 주석을 푼다.

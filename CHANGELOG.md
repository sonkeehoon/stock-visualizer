# Changelog

## [0.2.1] - 2025-11-25
### Fixed
- app.py 수정
    - 미국 주식 크롤링 함수(get_US_df) 버그 수정

## [0.2.1] - 2025-11-25
### Fixed
- crawler.py 수정
    - 환율 크롤링 함수(get_er_df) 오류 수정

## [0.2.0] - 2025-11-24
### Added
- `Exchange Rate` 탭 및 내용 추가

## [0.1.1] - 2025-10-30
### Fixed
- 탭 이름 변경
    - US Top100 -> U.S. Top100
- U.S. Top100 탭 속 데이터프레임 제목 수정
    - Nasdaq Top 100 -> U.S. Top 100
- img폴더에 워크플로우 이미지 수정
- README.md 속 워크플로우 이미지 수정

## [0.1.0] - 2025-10-29
### Fixed
- 0.0.9에서 크롤링 selector부분 오류 수정

## [0.0.9] - 2025-10-28
### Added
- 탭 추가
    - 기존 코스피 데이터는 'Kospi Top100'탭
        - 실시간 국내상장 상위 100개 기업 주가
    - 'US TOP100' 탭 추가
        - 실시간 미국상장 상위 100개 기업 주가
    - 'Exchange Rate' 탭 추가
        - 실시간 환율 (추가 예정)

## [0.0.8] - 2025-10-27
### Added
- 데이터프레임에 "현재가" 컬럼 추가
- .github/workflows 추가
    - deploy.yml: master에 커밋 시 자동 배포
    - format.yml: develop에 커밋 시 자동으로 코드 정리(black + isort)

## [0.0.5] - 2025-09-18
### Added
- 배포 환경에서 컨테이너를 제어하는 Makefile 추가

## [0.0.2] - 2025-09-18
### Fixed
- 첫 접속 시 최신 데이터가 표시되지 않던 버그 수정
- `crawler` 모듈을 함수형(`get_target_df`)으로 리팩터링하여 항상 실시간 데이터를 가져오도록 개선
- `importlib.reload` 불필요 코드 제거

## [0.0.1] - 2025-09-16
### First commit

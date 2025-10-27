# Changelog

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

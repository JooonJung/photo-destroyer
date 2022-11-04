# 🎞 photo-destroyer
사진부스 아카이빙 웹 프로젝트

## 컨벤션

### 코드 작성
- 변수, 함수, 인스턴스는 카멜 케이스 사용
  - ex) onClick, photoBoothType
- 함수명은 동사 + 명사 형태로 구성
  - ex) getUserId
  
### commit type
- FEAT : 기능 추가 (스타일의 변경을 포함함)
- FIX : 버그 수정
- DOCS : 문서 수정
- STYLE : 코드 포맷팅
- REFACT : 코드 리팩토링(결과의 변경 없이 코드의 구조를 재조정함)
- TEST : 테스트 코드
- CHORE : 빌드, 패키지 관련 수정

### Branch (Git-Flow)
- master : 기준이 되는 브랜치로 제품을 배포하는 브랜치
- develop : 개발 브랜치로 개발자들이 이 브랜치를 기준으로 각자 작업한 기능들을 Merge
- feature : 단위 기능을 개발하는 브랜치로 기능 개발이 완료되면 develop 브랜치에 Merge
- release : 배포를 위해 master 브랜치로 보내기 전에 먼저 QA(품질검사)를 하기위한 브랜치
- hotfix : master 브랜치로 배포를 했는데 버그가 생겼을 떄 긴급 수정하는 브랜치

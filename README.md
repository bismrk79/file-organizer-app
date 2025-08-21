# 파일정리기 Android App

## 📱 소개
파일명이 `abc-123.확장자` 패턴을 가진 파일들을 자동으로 정리하는 안드로이드 앱입니다.

## ✨ 주요 기능
- **패턴 매칭**: `abc-123.확장자` 형태의 파일 인식
- **자동 폴더 생성**: abc 부분으로 폴더명 생성
- **파일 이동**: 패턴에 맞는 폴더로 자동 이동
- **미리보기**: 실행 전 결과 확인
- **실시간 로그**: 작업 과정 상세 표시

## 📋 패턴 규칙
- **abc 부분**: 2-12자, 문자로 시작, 중간에 숫자 가능
- **하이픈 필수**: 반드시 `-` 포함
- **123 부분**: 2-10자 숫자, 추가로 `-d` 형태 가능

## 📱 APK 다운로드
[Releases 페이지](https://github.com/YOUR_USERNAME/YOUR_REPO/releases)에서 최신 APK를 다운로드하세요.

## 🚀 자동 빌드
이 프로젝트는 GitHub Actions를 통해 자동으로 APK를 빌드합니다.
- `main` 브랜치에 push할 때마다 자동 빌드
- Actions 탭에서 빌드 진행 상황 확인 가능

## 🔧 로컬 빌드 (선택사항)
```bash
# 의존성 설치
pip install -r requirements.txt

# APK 빌드
buildozer android debug
```

## 📁 프로젝트 구조
```
📁 project/
├── 📄 main.py              # 메인 앱 코드
├── 📄 buildozer.spec       # 빌드 설정
├── 📄 requirements.txt     # Python 의존성
├── 📄 .github/workflows/   # GitHub Actions
│   └── 📄 build.yml
└── 📄 README.md           # 이 파일
```

## 🛡️ 권한
- **READ_EXTERNAL_STORAGE**: 파일 읽기
- **WRITE_EXTERNAL_STORAGE**: 파일 쓰기/이동
- **MANAGE_EXTERNAL_STORAGE**: Android 11+ 지원

## 📞 문의
이슈나 질문이 있으시면 GitHub Issues를 이용해 주세요.
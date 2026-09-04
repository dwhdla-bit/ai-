# RI // NEON AI Discord Bot

검정 + 네온 게임 느낌의 Discord AI 챗봇.

## 명령어
- `/ai 질문` : AI와 대화
- `/help` : 도움말

## 필요한 환경변수
- `TOKEN` : Discord Bot Token
- `OPENROUTER_API_KEY` : OpenRouter API Key
- `MODEL` : 기본값 `openrouter/free`

## GitHub
모든 파일을 저장소 루트에 업로드.

## Render
New Blueprint로 GitHub 저장소를 연결하면 `render.yaml`이 서비스를 설정합니다. Render Environment Variables에 TOKEN과 OPENROUTER_API_KEY를 입력하세요.

## Discord 초대
봇을 초대할 때 `bot`과 `applications.commands` 스코프를 사용하세요. Slash Command(`/ai`) 방식입니다.

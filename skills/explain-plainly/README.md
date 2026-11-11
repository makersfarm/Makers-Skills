# Explain Plainly · 쉽게 풀어 설명

기술/데이터 근거로 한 설명을, 정보를 빼지 않고 **실제 업무·화면(UI) 용어로 재구성**한다. 사용자가 "무슨 말인지 모르겠다 / 이게 뭐냐 / 쉽게 / 일반 용어로"라고 되묻거나, 그 설명을 **고객사·현업·WMS/ERP 담당자·벤더에게 전달해 확인**받아야 할 때 사용한다.

## Install

From the repository root:

```bash
./scripts/install.sh skills explain-plainly
```

## Usage

```text
$explain-plainly 방금 설명을 비개발 현업이 이해할 수 있게 업무·화면 용어로 다시 풀어줘.
```

재구성 골격(필요한 항목만 골라 씀):

1. 한 줄 정의 — 업무어로 "이건 결국 ~다"
2. 어느 시스템 / 어느 데이터에서 나오나 (기술 식별자는 괄호 보조)
3. UI/업무 용어로는 어떻게 보이나 (화면 라벨·드롭다운·구분값 수준)
4. 실제로 관측된 값/증거 (상대가 매핑 가능하도록 구체값)
5. 왜 필요한가 (한 문장 비즈니스 동기)
6. 그대로 보낼 질문 문구 (인용블록, 업무어로만)
7. (선택) 한계/대안 (샘플·추정·미검증이면 명시)

정확성은 유지하고 추상화 수준만 바꾼다. 불확실한 내용을 쉬운 말로 바꾸며 단정으로 승격시키지 않는다.

## Files

- [SKILL.md](SKILL.md): Canonical reconstruction instructions.
- [agents/openai.yaml](agents/openai.yaml): Codex display metadata and example prompt.
- [Catalog](../../docs/skill-catalog.md) · [Changelog](../../CHANGELOG.md).

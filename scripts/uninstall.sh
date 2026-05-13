#!/usr/bin/env bash
set -euo pipefail

MANAGED_BY="makersfarm/Makers-Skills"

usage() {
  cat <<'EOF'
Usage:
  uninstall.sh skills ALL [--tools codex,agents,claude] [--project <dir>]
  uninstall.sh skills <name...> [--tools codex,agents,claude] [--project <dir>]
EOF
}

fail() {
  echo "error: $*" >&2
  exit 1
}

remove_skill() {
  local dest="$1"
  local name="$2"

  if [[ ! -e "$dest" ]]; then
    echo "skipped: $name -> $dest (not installed)"
    skipped=$((skipped + 1))
    return
  fi

  if [[ ! -f "$dest/.managed-by" ]] || [[ "$(cat "$dest/.managed-by")" != "$MANAGED_BY" ]]; then
    echo "skipped: $name -> $dest (unmanaged target)"
    skipped=$((skipped + 1))
    return
  fi

  rm -rf -- "$dest"
  echo "removed: $name -> $dest"
  removed=$((removed + 1))
}

collect_managed_skills() {
  local target_root="$1"

  [[ -d "$target_root" ]] || return

  find "$target_root" -mindepth 2 -maxdepth 2 -name .managed-by -type f | while IFS= read -r marker; do
    if [[ "$(cat "$marker")" == "$MANAGED_BY" ]]; then
      basename -- "$(dirname -- "$marker")"
    fi
  done
}

[[ "${1:-}" == "skills" ]] || {
  usage
  exit 1
}
shift

[[ "$#" -gt 0 ]] || {
  usage
  exit 1
}

requested=()
tools_csv="codex"
project_dir=""

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --tools)
      shift
      [[ "$#" -gt 0 ]] || fail "--tools requires a comma-separated value"
      tools_csv="$1"
      ;;
    --project)
      shift
      [[ "$#" -gt 0 ]] || fail "--project requires a directory"
      project_dir="$1"
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    --*)
      fail "unknown option: $1"
      ;;
    *)
      requested+=("$1")
      ;;
  esac
  shift
done

[[ "${#requested[@]}" -gt 0 ]] || fail "missing skill selection"

IFS=',' read -r -a tools <<< "$tools_csv"
targets=()
for tool in "${tools[@]}"; do
  tool="${tool//[[:space:]]/}"
  case "$tool" in
    codex)
      targets+=("$HOME/.codex/skills")
      ;;
    agents)
      [[ -n "$project_dir" ]] || fail "--tools agents requires --project <dir>"
      targets+=("$project_dir/.agents/skills")
      ;;
    claude)
      targets+=("$HOME/.claude/skills")
      ;;
    "")
      fail "empty tool in --tools"
      ;;
    *)
      fail "unsupported tool: $tool"
      ;;
  esac
done

skills=()
if [[ "${#requested[@]}" -eq 1 && "${requested[0]}" == "ALL" ]]; then
  while IFS= read -r skill; do
    skills+=("$skill")
  done < <(
    for target_root in "${targets[@]}"; do
      collect_managed_skills "$target_root"
    done | sort -u
  )
else
  skills=("${requested[@]}")
fi

removed=0
skipped=0

for skill in "${skills[@]}"; do
  for target_root in "${targets[@]}"; do
    remove_skill "$target_root/$skill" "$skill"
  done
done

echo "summary: removed=$removed skipped=$skipped"

#!/usr/bin/env bash
set -euo pipefail

MANAGED_BY="makersfarm/Makers-Skills"
REPO_URL="https://github.com/makersfarm/Makers-Skills.git"
ORIGINAL_ARGS=("$@")
SCRIPT_SOURCE="${BASH_SOURCE[0]-$0}"
SCRIPT_DIR="$(cd -- "$(dirname -- "$SCRIPT_SOURCE")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/.." && pwd)"
SKILLS_ROOT="$REPO_ROOT/skills"

usage() {
  cat <<'EOF'
Usage:
  install.sh skills ALL [--tools codex,agents,claude] [--project <dir>]
  install.sh skills <name...> [--tools codex,agents,claude] [--project <dir>]
  install.sh ALL [--tools codex,agents,claude] [--project <dir>]
  install.sh <name...> [--tools codex,agents,claude] [--project <dir>]
EOF
}

fail() {
  echo "error: $*" >&2
  exit 1
}

bootstrap_from_remote() {
  local cache_dir="${MAKERS_SKILLS_CACHE:-$HOME/.makers-skills}"

  if [[ -d "$cache_dir/.git" ]]; then
    git -C "$cache_dir" pull --quiet --ff-only
  else
    if [[ -e "$cache_dir" ]]; then
      fail "cache path exists but is not a git repository: $cache_dir"
    fi
    git clone --quiet --depth 1 "$REPO_URL" "$cache_dir"
  fi

  exec "$cache_dir/scripts/install.sh" "${ORIGINAL_ARGS[@]}"
}

copy_skill() {
  local src="$1"
  local dest="$2"
  local name="$3"
  local existed=0

  if [[ -e "$dest" ]]; then
    existed=1
    if [[ ! -f "$dest/.managed-by" ]] || [[ "$(cat "$dest/.managed-by")" != "$MANAGED_BY" ]]; then
      echo "skipped: $name -> $dest (unmanaged target exists)"
      skipped=$((skipped + 1))
      return
    fi
    rm -rf -- "$dest"
  fi

  mkdir -p -- "$(dirname -- "$dest")"
  cp -R -- "$src" "$dest"
  printf '%s\n' "$MANAGED_BY" > "$dest/.managed-by"

  if [[ "$existed" -eq 1 ]]; then
    echo "updated: $name -> $dest"
    updated=$((updated + 1))
  else
    echo "installed: $name -> $dest"
    installed=$((installed + 1))
  fi
}

if [[ ! -d "$SKILLS_ROOT" ]]; then
  bootstrap_from_remote
fi

if [[ "${1:-}" == "skills" ]]; then
  shift
fi

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
[[ -d "$SKILLS_ROOT" ]] || fail "skills directory not found: $SKILLS_ROOT"

skills=()
if [[ "${#requested[@]}" -eq 1 && "${requested[0]}" == "ALL" ]]; then
  while IFS= read -r skill_path; do
    skills+=("$(basename -- "$skill_path")")
  done < <(find "$SKILLS_ROOT" -mindepth 1 -maxdepth 1 -type d | sort)
else
  skills=("${requested[@]}")
fi

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

installed=0
updated=0
skipped=0

for skill in "${skills[@]}"; do
  src="$SKILLS_ROOT/$skill"
  if [[ ! -d "$src" ]]; then
    echo "skipped: $skill (skill not found)"
    skipped=$((skipped + ${#targets[@]}))
    continue
  fi

  for target_root in "${targets[@]}"; do
    copy_skill "$src" "$target_root/$skill" "$skill"
  done
done

echo "summary: installed=$installed updated=$updated skipped=$skipped"

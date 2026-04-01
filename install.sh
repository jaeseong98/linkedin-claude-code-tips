#!/usr/bin/env bash
# Claude Code Skills 설치 스크립트
# 사용법: bash install.sh

set -e

COMMANDS_DIR="$HOME/.claude/commands"
SKILLS_DIR="$(cd "$(dirname "$0")/generated_skills" && pwd)"

echo "🔧 Claude Code Skills 설치 시작..."
echo "   대상 디렉토리: $COMMANDS_DIR"
echo ""

mkdir -p "$COMMANDS_DIR"

installed=0
skipped=0

for date_dir in "$SKILLS_DIR"/*/; do
  date=$(basename "$date_dir")
  for skill_file in "$date_dir"*.md; do
    [ -f "$skill_file" ] || continue
    filename=$(basename "$skill_file")
    dest="$COMMANDS_DIR/$filename"

    if [ -f "$dest" ]; then
      echo "  ⏭  건너뜀 (이미 존재): $filename"
      ((skipped++)) || true
    else
      cp "$skill_file" "$dest"
      echo "  ✅ 설치: $filename"
      ((installed++)) || true
    fi
  done
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  설치 완료: ${installed}개 | 건너뜀: ${skipped}개"
echo "  Claude Code에서 /agent-, /config-, /skills- 등으로 사용 가능"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

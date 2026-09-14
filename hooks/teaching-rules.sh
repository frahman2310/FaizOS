#!/bin/bash
# UserPromptSubmit: put the ONE teaching method in front of Claude on every message.
# It injects the faiz-teach skill itself, so there is no second copy to drift. Fails open.
SKILL="/Users/faizr/AI OS for Learning/.claude/skills/faiz-teach/SKILL.md"
[ -f "$SKILL" ] && awk 'BEGIN{f=0} /^---$/{f++; next} f>=2' "$SKILL"
exit 0

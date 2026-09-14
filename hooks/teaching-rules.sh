#!/bin/bash
# UserPromptSubmit: put the teaching rules in front of Claude on every message.
# Fails open: a missing file never blocks a prompt.
cat "/Users/faizr/AI OS for Learning/docs/teaching-rules.md" 2>/dev/null
exit 0

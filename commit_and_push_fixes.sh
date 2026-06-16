#!/bin/bash
# ============================================================
# commit_and_push_fixes.sh — DEPRECATED
#
# This script performed a blind `git add .` and `git push` in
# every sub-repo whose working tree had changes. It was flagged
# in the audit (bd issue mcphub-7j8) for the same security
# risks as commit_all.sh (commits and pushes secret-containing
# files like .env, .p12, contacts.json if they ever end up
# staged).
#
# SAFE REPLACEMENT
# ----------------
# For each sub-repo that has changes:
#   cd <sub-repo>
#   git status                            # review changes
#   git add <file>                        # explicit staging
#   git diff --cached                     # final review
#   git commit -m "..."                   # descriptive message
#   git pull --rebase origin main         # catch up to remote
#   git push origin main                  # push
#
# For batch operations, build a custom script that does the
# above with --dry-run support and a confirmation prompt.
# ============================================================

echo "ERROR: commit_and_push_fixes.sh is deprecated. See comments above for the safe replacement."
echo "       (bd issue mcphub-7j8)"
exit 1

#!/bin/bash
# ============================================================
# commit_all.sh — DEPRECATED
#
# This script performed a blind `git add .` and `git push` in
# every sub-repo. It was identified as a security risk in the
# audit (bd issue mcphub-7j8) and has been neutralized.
#
# To sync changes safely, use:
#   1. `git status` to review what would be committed
#   2. `git add <specific-file>` to stage explicitly
#   3. `git commit -m "<descriptive message>"`
#   4. `git push origin main`
#
# For batch operations across sub-repos, use a custom script
# that follows the above pattern. NEVER use `git add .` blindly
# with sub-repos that may contain secrets in `.env` files.
# ============================================================

echo "ERROR: commit_all.sh is deprecated. See comments above for the safe replacement."
echo "       (bd issue mcphub-7j8)"
exit 1

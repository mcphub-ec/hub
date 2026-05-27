#!/bin/bash
find . -mindepth 2 -name ".git" -type d | while read gitdir; do
    repo_dir=$(dirname "$gitdir")
    echo "--- Processing $repo_dir ---"
    cd "$repo_dir"
    
    if ! git diff --quiet || ! git diff --cached --quiet || [ -n "$(git ls-files --others --exclude-standard)" ]; then
        git add .
        git commit -m "fix: resolve flake8 syntax errors and bandit false positives"
        git push
    else
        echo "No changes in $repo_dir"
    fi
    cd - > /dev/null
done

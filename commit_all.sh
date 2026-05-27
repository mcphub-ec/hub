#!/bin/bash
for d in comunicaciones/email contabilidad/* pagos/*; do
  if [ -d "$d" ]; then
    echo "--- Processing $d ---"
    cd "$d"
    
    # Check if there are changes
    if ! git diff-index --quiet HEAD --; then
      git add .
      git commit -m "fix: resolve Bandit false positives and pause automated docker publish"
      git push origin main
    else
      echo "No changes to commit in $d"
    fi
    cd - > /dev/null
  fi
done

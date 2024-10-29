#!/bin/bash

if grep -q _enter *.md ; then
  echo "Replace all text having _enter with your input"
  exit 1
fi

echo "All reflections are complete!"
exit 0

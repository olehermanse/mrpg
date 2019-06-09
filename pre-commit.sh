#!/bin/sh
#
# Run format and test before commiting
#   cp -a pre-commit.sh .git/hooks/pre-commit

fail=0

RED='\033[0;31m'
NC='\033[0m' # No Color

yapf --recursive . --diff --parallel || fail="${RED}Commit hook failed: Formatting - run make yapf${NC}"
test "$fail" = 0                     || echo $fail
test "$fail" = 0                     || exit 1

py.test                              || fail="${RED}Commit hook failed: Formatting - run make check${NC}"
test "$fail" = 0                     || echo $fail
test "$fail" = 0                     || exit 1

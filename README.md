# Advent of Code 2023

Back again.

https://adventofcode.com/2023/

Run tests with:
```
./Taskfile
```

This runs mypy, pytest. Also set up the repo with the precommit check
```
./Taskfile initrepo
```

Make sure rust and python are formatted in a standard way:
```
./Taskfile fmt
```

Puzzle input shouldn't be shared, so it is not committed to the repo.
Use [aoc-cli](https://github.com/scarvalhojr/aoc-cli) to download input for a given day:
```
aoc download -I --input-file -d {day-num} input/real/${DAY}
```
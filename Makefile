default: run

run:
	python3 -m mrpg

yapf:
	yapf --recursive . -i

fmt: yapf
format: yapf

.PHONY: default run fmt format yapf

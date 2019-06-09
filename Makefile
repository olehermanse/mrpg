default: run

run:
	python3 -m mrpg

terminal:
	python3 -m mrpg --terminal

yapf:
	yapf --recursive . -i

fmt: yapf
format: yapf

check:
	py.test
test: check

.PHONY: default run fmt format yapf terminal test check

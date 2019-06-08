default: run

run:
	python3 -m mrpg

terminal:
	python3 -m mrpg --terminal

yapf:
	yapf --recursive . -i

fmt: yapf
format: yapf

.PHONY: default run fmt format yapf terminal

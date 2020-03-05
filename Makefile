default: run

run:
	python3 -m mrpg

terminal:
	python3 -m mrpg --terminal

format:
	black .

check:
	py.test

.PHONY: default run format terminal check

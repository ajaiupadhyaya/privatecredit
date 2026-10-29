PYTHON ?= python3
.PHONY: build test serve
build:
	$(PYTHON) scripts/build_portfolio.py
test: build
	$(PYTHON) -m pytest tests -q
	node --test frontend/tests/*.test.cjs
serve:
	$(PYTHON) -m http.server 4173 --bind 127.0.0.1 --directory dist

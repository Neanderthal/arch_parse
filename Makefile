PORT ?= 8000
HOST ?= 0.0.0.0
DEFAULT_PAGE ?= index.html

.PHONY: serve
serve:
	@echo "Starting local server at http://$(HOST):$(PORT) (open $(DEFAULT_PAGE))"
	python3 -m http.server $(PORT) --bind $(HOST)

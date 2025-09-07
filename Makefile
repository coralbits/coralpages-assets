.PHONY: help clean run test test-watch

help:
	@echo "Usage: make <target>"
	@echo "Targets:"
	@echo "  help - Show this help message"
	@echo "  clean - Clean the project"
	@echo "  run - Run the project"
	@echo "  test - Run tests"
	@echo "  test-watch - Run tests and watch for changes"

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache

run:
	uv run uvicorn serve:app --host 0.0.0.0 --port 8004 --reload

test:
	uv run pytest

test-watch:
	while true; do \
		uv run pytest; \
		inotifywait -e modify -r .; \
		sleep 1; \
	done
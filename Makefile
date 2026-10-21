.PHONY: score clean

score:
	uv run python score.py

clean:
	rm -f output/*.csv

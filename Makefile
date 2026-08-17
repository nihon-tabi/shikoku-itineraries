# Everything in out/ is generated from src/. Never edit it by hand.
PY := .venv/bin/python

.PHONY: all sheets dashboard map geocode clean setup

all: sheets dashboard map      ## rebuild every deliverable

sheets:                        ## the four .xlsx workbooks + CSVs -> out/sheets/
	$(PY) -m src.build_sheets
	$(PY) -m src.build_shimanami

dashboard:                     ## dashboard.html + standalone -> out/
	$(PY) -m src.build_dashboard

map:                           ## sights-only KML + CSV for Google My Maps
	$(PY) -m src.build_map

geocode:                       ## resolve any new PLACES entries (costs API calls)
	$(PY) -m src.geocode

setup:                         ## create the venv
	python3 -m venv .venv && $(PY) -m pip install -q -r requirements.txt

clean:
	rm -rf out __pycache__ src/__pycache__ src/refs/__pycache__

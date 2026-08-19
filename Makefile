# Everything in out/ is generated from src/. Never edit it by hand.
# Override for CI, which installs into the system interpreter:  make PY=python
PY ?= .venv/bin/python

.PHONY: all sheets dashboard map mymaps places mapcodes trailheads geocode clean setup

all: sheets dashboard map mymaps   ## rebuild every deliverable

sheets:                        ## the four .xlsx workbooks + CSVs -> out/sheets/
	$(PY) -m src.build_sheets
	$(PY) -m src.build_shimanami

dashboard:                     ## dashboard.html + standalone -> out/
	$(PY) -m src.build_dashboard

map:                           ## sights-only KML + CSV for Google My Maps
	$(PY) -m src.build_map

# The full map: every place across all four options, in the house entry format.
# Built by the japan-my-maps skill so the KML conventions live in one place.
SKILL ?= $(HOME)/projects/japan-trip-planner/.claude/skills/japan-my-maps
mymaps:                        ## full categorised map -> out/shikoku-map.kmz
	$(PY) -m src.build_mymaps
	$(PY) $(SKILL)/scripts/build_map.py out/shikoku-mymaps.json out/shikoku-map

places:                        ## refresh address/phone/website from Google (costs API calls)
	$(PY) -m src.fetch_places

mapcodes:                      ## fetch any missing Denso map codes
	$(PY) -m src.fetch_mapcodes

trailheads:                    ## check no trailhead contradicts its own description
	$(PY) -m src.check_trailheads

geocode:                       ## resolve any new PLACES entries (costs API calls)
	$(PY) -m src.geocode

setup:                         ## create the venv
	python3 -m venv .venv && $(PY) -m pip install -q -r requirements.txt

clean:
	rm -rf out __pycache__ src/__pycache__ src/refs/__pycache__

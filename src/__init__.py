"""Shikoku itineraries — the single source of truth and the generators that
render it into out/.

Run the builders from the project root as modules, or just use `make`:

    python -m src.build_sheets       # the .xlsx workbooks + CSVs
    python -m src.build_shimanami    # the Shimanami Kaido variants workbook
    python -m src.build_dashboard    # the HTML dashboard, both flavours
    python -m src.geocode            # resolve new PLACES entries (API calls)
"""

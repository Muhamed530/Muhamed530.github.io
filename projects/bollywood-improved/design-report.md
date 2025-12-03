# Bollywood — Improved Dashboard (Design Report)

## Audience & Purpose
- Primary audience: Studio executives and entertainment analysts who need a quick way to evaluate actors for casting and marketing decisions.
- Purpose: Support decisions by surfacing actors who balance public attention (fame) with demonstrated performance (talent).

## KPIs
- Fame Score — composite proxy for public attention (normalized).
- Talent Score — normalized rating-based performance measure.
- Balance Score — closeness between fame and talent (higher = better alignment).

## Story Mode
- Guided 5-step narrative built into the Streamlit app (Overview → Stars → Hidden Gems → Compare → Export).
- Each step focuses the user's attention on a single task, with pre-filtered views and short narrative text.

## Dashboard Structure
- Top row: KPI cards (Avg Fame, Avg Talent, Avg Balance).
- Main area: Fame vs Talent scatter (interactive, hover details).
- Supporting panels: Top lists, hidden-gems table, compare view, and export button.

## Data Cleaning
- Convert numeric KPI columns to numeric types and coerce errors.
- Filter nulls for critical columns before visualization.

## Design Choices
- Palette: cinematic warm accent for highlights; neutral background for charts.
- Visual hierarchy: KPIs → primary scatter → supporting tables.
- Interactivity: filters in sidebar; Story Mode steppers; Plotly hovertemplates for detail-on-demand.

## Reflection & Next Steps
- What worked: Story Mode provides an onboarding narrative; KPI focus reduces cognitive load.
- Improvements: Add mobile-responsive chart layouts, time-series tracking, and side-by-side comparison visuals.

## Reproducibility
- Files in folder: `streamlit_app.py`, `design-report.md`.
- Expected dataset path: `projects/bollywood-dashboard/BollywoodActorRanking.csv` (copy into that location or update path in `streamlit_app.py`).
- Run locally:
```
pip install -r requirements.txt
streamlit run streamlit_app.py
```

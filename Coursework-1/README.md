# COMP0035 Coursework 1 - (Chen123-hongtai)

## Overview
This repository contains code to:
- explore an assigned dataset (`src/data_explore.py`)
- prepare the data for three example questions (`src/data_prep.py`)
- create an SQLite database from prepared CSVs (`src/create_db.py`)

## How to run (Windows 11, VS Code)
1. Clone your GitHub Classroom repo.
2. Put the dataset file into `data/dataset.csv` (or `dataset.xlsx`).
3. Create and activate virtualenv:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt

Run these four scripts in order:
1."parse_international_visitors.py"
2."explore_international_visitors.py"
3."prepare_views.py"
4."create_db.py"

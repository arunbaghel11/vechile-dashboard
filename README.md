# 🚗 Vahan Registration Dashboard

This project scrapes, processes, and visualizes vehicle registration data from the Indian Vahan public dashboard.

---

## Features

- **Automated Data Scraping:**  
  Collects vehicle registration statistics by vehicle class from the Vahan portal.

- **Data Processing:**  
  Transforms raw data, adds growth metrics, and prepares it for analysis.

- **Interactive Dashboard:**  
  Visualizes trends using Streamlit and Plotly, with filters for category, manufacturer, and date range.

---

## Folder Structure

```
data/
  ├─ vehicle_class_group.csv           # Raw scraped data
  ├─ processed_vehicle_type.csv        # Processed data for dashboard
  └─ README.md                         # This file

scripts/
  ├─ scrape_vahan.py                   # Scrapes Vahan dashboard data
  └─ process_data.py                   # Processes and transforms data

utils/
  └─ helpers.py                        # Helper functions for loading and plotting

app.py                                 # Streamlit dashboard
```

---

## How to Run

1. **Install dependencies:**
   ```powershell
   pip install selenium beautifulsoup4 pandas streamlit plotly
   ```

2. **Scrape the data:**
   ```powershell
   python scripts/scrape_vahan.py
   ```
   - Scrapes latest data and saves to `data/vehicle_class_group.csv`.

3. **Process the data:**
   ```powershell
   python scripts/process_data.py
   ```
   - Transforms data and creates `data/processed_vehicle_type.csv`.

4. **Launch the dashboard:**
   ```powershell
   streamlit run app.py
   ```
   - Opens the dashboard in your browser.

---

## Project Workflow

1. **Data Collection:**  
   Scrape vehicle registration data from Vahan.

2. **Data Processing:**  
   Clean and reshape data, add YoY and QoQ growth columns.

3. **Visualization:**  
   Explore trends interactively by category and manufacturer.

---

## Requirements

- Python 3.8+
- Chrome browser (for Selenium)
- Internet connection (for scraping)

---

## Notes

- Manufacturer data is not scraped by default; dashboard will show a warning if missing.
- Growth metrics require historical data (multiple dates).


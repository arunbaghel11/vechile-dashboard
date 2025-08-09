"""
Scrapes Vahan public dashboard tables for:
  • Vehicle Class Wise Vehicle Category Group Data
Outputs one CSV in ../data/
"""
import os, re, time
from datetime import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE = "https://vahan.parivahan.gov.in/vahan4dashboard/vahan/view/reportview.xhtml"
OUTDIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUTDIR, exist_ok=True)

def _clean(num):
    return int(re.sub(r"[^\d]", "", num)) if num else 0

def fetch_vchgroup_table(driver, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.ID, "vchgroupTable"))
        )
    except Exception:
        with open("debug_vahan.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise ValueError("Table 'vchgroupTable' not found in page.")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("div", {"id": "vchgroupTable"})
    if table is None:
        with open("debug_vahan.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        raise ValueError("Table 'vchgroupTable' not found in page.")

    # Find the tbody with data
    tbody = table.find("tbody", {"id": "vchgroupTable_data"})
    rows = []
    for tr in tbody.find_all("tr"):
        cells = [td.get_text(strip=True) for td in tr.find_all("td")]
        rows.append(cells)
    # Find headers
    thead = table.find("thead", {"id": "vchgroupTable_head"})
    header_rows = thead.find_all("tr")
    # Flatten header
    headers = []
    for th in header_rows[-1].find_all("th"):
        headers.append(th.get_text(strip=True))
    # Prepend S No and Vehicle Class columns
    headers = ["S No", "Vehicle Class"] + headers[2:]
    return headers, rows

def scrape_vehicle_class_group(driver):
    headers, rows = fetch_vchgroup_table(driver)
    # The columns are: S No, Vehicle Class, 4WIC, LMV, MMV, HMV, TOTAL
    data = []
    for r in rows:
        if len(r) < 7:
            continue
        data.append({
            "S No": r[0],
            "Vehicle Class": r[1],
            "4WIC": _clean(r[2]),
            "LMV": _clean(r[3]),
            "MMV": _clean(r[4]),
            "HMV": _clean(r[5]),
            "TOTAL": _clean(r[6])
        })
    pd.DataFrame(data).to_csv(f"{OUTDIR}/vehicle_class_group.csv", index=False)

def main():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(BASE)
    time.sleep(5)
    # Optionally, click the main "Refresh" button if needed
    try:
        refresh_btn = driver.find_element(By.XPATH, "//button[span[contains(text(),'Refresh')]]")
        refresh_btn.click()
        time.sleep(5)
    except Exception:
        pass
    scrape_vehicle_class_group(driver)
    driver.quit()
    print("Scraping complete. CSV saved to data/vehicle_class_group.csv")

if __name__ == "__main__":
    main()
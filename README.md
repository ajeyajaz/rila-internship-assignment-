
# CPWD Tender Scraper

## 📌 Task
This Python script scrapes the first 20 tenders from the "New Tenders → All" section.

🔗 Website: https://etender.cpwd.gov.in/

---

## 📊 Data Collected

| Website Column                          | CSV Column Name           |
|----------------------------------------|----------------------------|
| NIT/RFP NO                             | ref_no                     |
| Name of Work / Subwork / Packages      | title                      |
| Estimated Cost                         | tender_value               |
| Bid Submission Closing Date & Time     | bid_submission_end_date    |
| EMD Amount                             | emd                        |
| Bid Opening Date & Time                | bid_open_date              |

---

## ▶️ How to Run

### 1. Install Required Packages

```bash
pip install -r requirements.txt
```

### 2. Run the Script

```bash
python main.py
```

After execution, a file named `tenders.csv` will be created with the extracted data.

---

## 📁 Files Included

- `main.py` – Main scraping script
- `requirements.txt` – Required Python packages
- `README.md` – This documentation



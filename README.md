# Government-Tender-Tracker-Bid-Match-Recommender App

This project is a smart government tender tracking and bid matching system that:
- Scrapes Indian e-procurement portals in real-time.
- Uses NLP to match tenders to company profiles.
- Displays relevant tenders via an interactive web app.
- Optionally sends email alerts for high-relevance matches.

---

## 📄 Table of Contents

- About
- Features
- Tech Stack
- Installation
- Usage
- Configuration
- Screenshots
- License
- Contact

---

## 🔍 About

Manual tracking of government tenders across multiple platforms is tedious and inefficient. This project automates the process of:
- Scraping tenders from official portals,
- Filtering tenders using AI-based semantic matching,
- Visualizing and notifying stakeholders.

It helps companies identify relevant tender opportunities efficiently and accurately.

---

## ✨ Features

- 🕷 Automated web scraping from major tender portals (NIC, Tamil Nadu, Kerala, etc.)
- 🔎 NLP-based semantic matching using `SentenceTransformer` models
- 📤 Real-time email alerts for matched tenders (optional)
- 📊 Interactive tender view in Streamlit interface
- 🧾 CSV-based logging and tracking of fetched tenders
- ⏱ Periodic scraping (every 15 minutes by default)

---

## 🧰 Tech Stack

| Component             | Description                          |
|-----------------------|--------------------------------------|
| Python                | Core programming language            |
| Selenium              | Web scraping from dynamic websites   |
| Pandas                | Data processing and CSV handling     |
| Streamlit             | Web dashboard for tender viewing     |
| SentenceTransformers  | NLP matching for tender filtering    |
| smtplib/email.message | For sending email alerts             |

---

##  Installation

1. **Clone the repository**

     git clone https://github.com/yourusername/tender-matcher.git

     cd tender-matcher 

2. **Install dependencies**

     pip install -r requirements.txt

## Usage
1. **Start the Scraper**
    Fetches tenders from listed portals and logs them to tenders.csv.
    python scraper.py
    The scraper runs continuously and updates data every 15 minutes.

2. **Run the Streamlit App**
    Launches the dashboard interface.
    streamlit run matcher_app.py
    Here you can:
    
    Enter your company's domain of expertise
    
    View relevant tenders sorted by match %
    
    Set up email notifications

## Configuration
 **Email Setup**
    In matcher_app.py, configure your email details:
    
    sender_email = "your-email@gmail.com"
    sender_app_password = "your-app-password"
    Note: Use an App Password if using Gmail.

**Matching Threshold**
    Adjust the similarity threshold in match_tenders() function in app.py:
    
    threshold = 0.5  # Lower = more matches, Higher = stricter

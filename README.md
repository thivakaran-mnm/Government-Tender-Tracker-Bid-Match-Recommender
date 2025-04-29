# Government-Tender-Tracker-Bid-Match-Recommender App

This project is a smart government tender tracking and bid matching system that:
- Scrapes Indian e-procurement portals in real-time.
- Uses NLP to match tenders to company profiles.
- Displays relevant tenders via an interactive web app.
- Optionally sends email alerts for high-relevance matches.

---

## 📄 Table of Contents

- [🔍 About](#-about)
- [✨ Features](#-features)
- [🧰 Tech Stack](#-tech-stack)
- [⚙️ Installation](#️-installation)
- [🚀 Usage](#-usage)
- [🛠 Configuration](#-configuration)
- [📷 Screenshots](#-screenshots)
- [🧾 License](#-license)
- [📬 Contact](#-contact)

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

## ⚙️ Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/tender-matcher.git
cd tender-matcher

import streamlit as st
import pandas as pd
import smtplib
from sentence_transformers import SentenceTransformer, util
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Functions to load company profile
def load_company_profile(profile_file=None):

    if profile_file:
        return profile_file
    return ""

def load_tenders(tender_file="/content/tenders.csv"):
    
    try:
        return pd.read_csv(tender_file)
    except Exception as e:
        st.error(f"Failed to load tenders: {e}")
        return pd.DataFrame()

# Functions for matching tenders with profile
def match_tenders(tenders, company_profile, threshold=0.36):
    
    if tenders.empty:
        return pd.DataFrame()

    tender_texts = tenders["Tender Title"].fillna("").tolist()

    # Encode titles and profile
    tender_embeddings = model.encode(tender_texts, convert_to_tensor=True)
    company_embedding = model.encode(company_profile, convert_to_tensor=True)

    # Calculate cosine similarity
    similarities = util.cos_sim(company_embedding, tender_embeddings).cpu().numpy().flatten()

    # Adding similarity scores
    tenders["Match Score"] = similarities

    matched = tenders[tenders["Match Score"] >= threshold]

    # Sorting by Match Score
    matched = matched.sort_values(by="Match Score", ascending=False)

    return matched

# email notifications
def send_email_alert(tender_title, receiver_email, sender_email, sender_app_password):
    """Send Email alert using Gmail SMTP"""
    try:
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = 'New Government Tender Match Alert!'

        body = f"""
        Hello,

        A new tender matches your company profile!

        Tender Title: {tender_title}

        Please check the tender portal for more details.

        Regards,
        Tender Tracker Bot
        """
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Upgrade the connection to secure
        server.login(sender_email, sender_app_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print(f"✅ Email sent to {receiver_email}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Streamlit app functions
def load_tenders_data():
    tenders = load_tenders()
    if tenders.empty:
        st.warning("Tender list is empty. Please upload a valid tenders.csv.")
    return tenders

def display_company_profile():
    st.sidebar.title("Company Profile Upload")
    uploaded_file = st.sidebar.file_uploader("Upload company profile (.txt)", type=["txt"])

    if uploaded_file:
        company_profile_text = uploaded_file.read().decode("utf-8")
        st.sidebar.write(company_profile_text)
        return company_profile_text
    else:
        st.sidebar.info("Please upload your company profile to get matched tenders.")
        return None

def send_notifications(matched, receiver_email):
    sender_email = "karan6thiva@gmail.com"  
    sender_app_password = "axbs uzag mmqi ****"  

    for _, row in matched.iterrows():
        if row["Match Score"] >= 0.5:
            send_email_alert(
                tender_title=row["Tender Title"],
                receiver_email=receiver_email,
                sender_email=sender_email,
                sender_app_password=sender_app_password
            )
            st.success(f"Notification sent for: {row['Tender Title']} to {receiver_email}")

# Streamlit app main function
def main():
    st.title("Government Tender Tracker & Bid Matching App")

    tenders = load_tenders_data()

    if tenders.empty:
        return
    
    receiver_email = st.sidebar.text_input("Enter your email to receive alerts", placeholder="you@example.com")

    st.subheader("📋 Available Tenders")
    st.dataframe(tenders)

    company_profile = display_company_profile()

    if company_profile:
        matched = match_tenders(tenders, company_profile)

        st.subheader("🎯 Matched Tenders")
        st.dataframe(matched)

        if st.button("Send Email Notifications"):
            send_notifications(matched,receiver_email)

if __name__ == "__main__":
    main()

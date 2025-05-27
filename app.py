import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from datetime import datetime, date

# Load credentials from Streamlit secrets
creds_dict = json.loads(st.secrets["GOOGLE_SHEET_CREDS"])

# Authorize with gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Connect to the correct spreadsheet and worksheet
spreadsheet = client.open("ICH-Customers")
sheet = spreadsheet.worksheet("sheet1")  # Make sure the sheet name is exactly "sheet1"

# Streamlit UI
st.set_page_config(page_title="Feedback | Indian Coffee House Ballygunge", layout="centered")
st.title("☕ Indian Coffee House Ballygunge")
st.subheader("📋 Guest Feedback Form")

with st.form("feedback_form"):
    name = st.text_input("Name*", max_chars=100)
    phone = st.text_input("Phone Number*", max_chars=10, help="Enter a valid 10-digit number")
    review = st.text_area("Your Review*", height=100)
    birthday = st.date_input("Birthday (optional)", value=None)
    anniversary = st.date_input("Anniversary (optional)", value=None)
    frequency = st.selectbox(
        "How often do you visit us?",
        ["Select an option", "First Time Guest", "Frequent Visitor", "Once in a while companion"]
    )
    
    submit = st.form_submit_button("Submit")

    if submit:
        if not name or not phone or not review:
            st.error("Please fill all required fields.")
        elif not (phone.isdigit() and len(phone) == 10):
            st.error("Phone number must be a 10-digit number.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = [
                name,
                phone,
                review,
                str(birthday) if birthday != date.today() else "",
                str(anniversary) if anniversary != date.today() else "",
                frequency if frequency != "Select an option" else "",
                timestamp
            ]
            sheet.append_row(data)
            st.success("✅ Thank you! Your feedback has been recorded.")

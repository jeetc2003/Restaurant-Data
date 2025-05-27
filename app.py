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
sheet = spreadsheet.worksheet("sheet1")

# Streamlit UI config
st.set_page_config(page_title="Feedback | Indian Coffee House Ballygunge", layout="centered", page_icon="☕")

# Header
st.markdown("""
    <div style='text-align: center; padding: 10px 0;'>
        <h1 style='font-size: 48px;'>☕ Indian Coffee House Ballygunge</h1>
        <h3 style='color: #6c757d;'>Your voice makes our brew better! 🍵</h3>
        <hr style='margin-top: 10px; border: 1px solid #ddd;'/>
    </div>
""", unsafe_allow_html=True)

st.markdown("### 📝 **Guest Feedback Form**")

with st.form("feedback_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("🙋 Your Name*", max_chars=100, placeholder="e.g. Suman Das")
        phone = st.text_input("📱 Phone Number*", max_chars=10, placeholder="10-digit number", help="Required to contact you for offers & rewards!")
        birthday = st.date_input("🎂 Birthday (optional)")
    
    with col2:
        anniversary = st.date_input("💍 Anniversary (optional)")
        frequency = st.selectbox(
            "🔁 How often do you visit us?",
            ["Select an option", "✨ First Time Guest", "💖 Frequent Visitor", "👋 Once in a while companion"]
        )

    review = st.text_area("🗣️ Your Thoughts*", height=120, placeholder="Share what you loved or what we can improve...")

    submit = st.form_submit_button("🚀 Submit Feedback")

    if submit:
        if not name or not phone or not review:
            st.error("⚠️ Please fill out all *required fields.")
        elif not (phone.isdigit() and len(phone) == 10):
            st.error("🚫 Phone number must be exactly 10 digits.")
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
            st.success("🎉 Thank you! Your feedback has been recorded.")
            st.toast("✅ Successfully submitted!", icon="🧾")
            st.balloons()

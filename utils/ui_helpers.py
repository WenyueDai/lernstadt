import streamlit as st
import datetime
import pytz

def set_page():
    today = datetime.date.today()
    uk_tz = pytz.timezone("Europe/London")
    now_uk = datetime.datetime.now(uk_tz)
    current_time_str = now_uk.strftime("%H:%M")
    st.set_page_config(page_title="Lernstadt Detective", layout="wide")
    st.title("Lernstadt Detective")
    st.markdown(f"### {today.strftime('%A, %d %B %Y')}, {current_time_str}")
    return today, today.isoformat(), current_time_str

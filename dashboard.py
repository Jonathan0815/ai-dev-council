import streamlit as st
import requests

st.set_page_config(page_title="Your AI Software Company", layout="wide")
st.title("🚀 Your Autonomous AI Dev Council")

idea = st.text_area("What shall we build today?", height=150, placeholder="e.g. Real-time Arc B580 GPU monitor with tray icon, web dashboard, iOS widget, Android notification")

if st.button("🚀 Build & Publish to GitHub", type="primary"):
    if idea.strip():
        with st.spinner("Council is thinking... (this takes 5–20 minutes)"):
            try:
                r = requests.post("http://localhost:8000/build", json={"idea": idea})
                r.raise_for_status()
                result = r.json()["result"]
                st.success("Council finished! Here's what they built:")
                st.markdown(result)
            except Exception as e:
                st.error(f"Council error: {e}")
    else:
        st.error("Enter an idea!")

st.markdown("---")
st.caption("Your private AI software company — running 100% locally on your Intel Arc B580")

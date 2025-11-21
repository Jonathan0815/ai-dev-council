import streamlit as st
from app_dev_crew import run_council

st.set_page_config(page_title="AI Dev Council", layout="wide")
st.title("Local AI Development Council")
st.write("Your Intel Arc B580 is powering this — 100% offline")

task = st.text_area("What do you want the council to build?", height=150)
if st.button("Start Council", type="primary"):
    if task.strip():
        with st.spinner("Council is working..."):
            result = run_council(task)
        st.success("Done!")
        st.markdown(result)
    else:
        st.warning("Enter a task first!")

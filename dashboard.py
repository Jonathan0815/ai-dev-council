import streamlit as st
import subprocess
import json
import os
import time

CODE_DIR = "generated_code"
LOG_FILE = "council_logs.json"
os.makedirs(CODE_DIR, exist_ok=True)

# Session state
for k in ["current_code", "last_result", "theme"]:
    if k not in st.session_state:
        st.session_state[k] = "" if k != "theme" else "dark"

# Theme
if st.session_state.theme == "dark":
    st.markdown("<style> .stApp { background: #0e1117; color: white; } </style>", unsafe_allow_html=True)

st.set_page_config(page_title="AI Dev Council v1.7", layout="wide")
st.title("AI Dev Council v1.7 — Clean & Focused")
st.caption("Council heartbeat • Fully local • 14B qwen2.5-coder")

# Sidebar
with st.sidebar:
    st.header("Theme")
    st.session_state.theme = st.selectbox("Mode", ["dark", "light"], index=0 if st.session_state.theme=="dark" else 1)
    
    st.header("Logs")
    if st.button("Clear logs"):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        st.success("Logs cleared")
        st.rerun()
    
    if os.path.exists(LOG_FILE):
        try:
            logs = json.load(open(LOG_FILE))
            for entry in logs[-15:]:
                avatar = {"PM": "PM", "Senior Developer": "Coder", "QA Engineer": "QA", "Council": "Council", "Result": "Result"}.get(entry["agent"], "AI")
                with st.chat_message(entry["agent"], avatar=avatar):
                    st.write(f"**{entry['agent']}** – {entry['timestamp']}")
                    st.caption(entry["content"])
        except:
            st.write("No valid logs")
    else:
        st.write("No logs yet")
    
    st.header("Task History")
    if os.path.exists(LOG_FILE):
        tasks = {e["task"]: e["task"] for e in logs if e["task"] != "unknown"}
        chosen = st.selectbox("Reload past task", [""] + list(tasks.keys()))
        if chosen:
            st.session_state.task_input = chosen

# Main area
col1, col2 = st.columns([3,1])
with col1:
    st.subheader("Code Editor")
    code = st.text_area("Edit / paste code", st.session_state.current_code, height=600)
    st.session_state.current_code = code

with col2:
    if st.button("Run Code", type="primary"):
        with st.spinner("Running..."):
            res = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=30)
            if res.stdout: st.code(res.stdout)
            if res.stderr: st.error(res.stderr)
    
    if st.button("Save as .py"):
        name = st.text_input("Filename", "script.py")
        if st.button("Save"):
            with open(os.path.join(CODE_DIR, name), "w") as f:
                f.write(code)
            st.success(f"Saved {name}")
            st.rerun()

# Council input
st.subheader("Task for the Council")
task = st.text_area("Your task", value=st.session_state.get("task_input",""), height=120, key="task_input")
if st.button("Start Council"):
    with st.spinner("Council is working..."):
        from app_dev_crew import run_council
        result = run_council(task)
        st.session_state.last_result = result
        st.success("Done!")
        st.rerun()  # Auto-refresh logs

if st.session_state.last_result:
    st.subheader("Result")
    st.markdown(st.session_state.last_result)

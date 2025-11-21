import streamlit as st
import subprocess
import json
import os
import time

# Config
CODE_DIR = "generated_code"
LOG_FILE = "council_logs.json"
os.makedirs(CODE_DIR, exist_ok=True)

# Session state
if 'current_code' not in st.session_state:
    st.session_state.current_code = ""
if 'last_result' not in st.session_state:
    st.session_state.last_result = ""

st.set_page_config(page_title="AI Dev Council v1.5", layout="wide")
st.title("AI Dev Council v1.5 — Fully Local")
st.markdown("**Council Status: Evolving...** | Arc B580 | 14B qwen2.5-coder")

# Sidebar
st.sidebar.title("Controls")

# Theme toggle
theme = st.sidebar.selectbox("Theme", ["Light", "Dark"], index=0)
if theme == "Dark":
    st.markdown("""
    <style>
        .stApp { background-color: #0e1117; color: white; }
        .stTextInput > div > div > input { background-color: #1e1e1e; color: white; }
    </style>
    """, unsafe_allow_html=True)

# File explorer
st.sidebar.subheader("Files")
py_files = [f for f in os.listdir(CODE_DIR) if f.endswith('.py')]
if py_files:
    selected_file = st.sidebar.selectbox("Open file", py_files)
    if selected_file:
        path = os.path.join(CODE_DIR, selected_file)
        with open(path, 'r') as f:
            st.session_state.current_code = f.read()
        st.sidebar.success(f"Loaded {selected_file}")

# GPU stats
st.sidebar.subheader("GPU")
try:
    out = subprocess.run(["intel_gpu_top", "-J"], capture_output=True, text=True, timeout=3)
    data = json.loads(out.stdout)
    usage = data.get("engines", [{}])[0].get("busy", "N/A")
    st.sidebar.metric("Usage", f"{usage}%")
except:
    st.sidebar.write("—")

# Main editor (native Streamlit — no external deps)
col1, col2 = st.columns([3, 1])
with col1:
    st.subheader("Code Editor")
    code = st.text_area(
        "Edit code here",
        value=st.session_state.current_code,
        height=600,
        help="Write Python code. Hit 'Run' to execute."
    )
    st.session_state.current_code = code

with col2:
    st.subheader("Actions")
    if st.button("Run Code", type="primary"):
        with st.spinner("Executing..."):
            try:
                res = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=30)
                if res.stdout:
                    st.success("Output:")
                    st.code(res.stdout)
                if res.stderr:
                    st.error("Error:")
                    st.code(res.stderr)
            except Exception as e:
                st.error(f"Run failed: {e}")

    if st.button("Save File"):
        name = st.text_input("Filename (e.g., script.py)", value="script.py")
        if name:
            path = os.path.join(CODE_DIR, name)
            with open(path, "w") as f:
                f.write(code)
            st.success(f"Saved {name}")
            st.rerun()

# Council task
st.subheader("Feed the Council")
task = st.text_area("Task description", height=120, placeholder="e.g. 'Build a simple calculator CLI'")
if st.button("Start Council"):
    with st.spinner("Council thinking..."):
        from app_dev_crew import run_council
        result = run_council(task)
        st.session_state.last_result = result
        st.markdown(result)

if st.session_state.last_result:
    st.subheader("Council Result")
    st.markdown(st.session_state.last_result)

# Evolution
st.subheader("Self-Evolution")
if st.button("Evolve to v2.0 (Pure Python)"):
    st.balloons()
    st.info("v1.6 will generate your successor here...")

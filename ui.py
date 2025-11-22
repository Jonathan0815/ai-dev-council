from http.server import BaseHTTPRequestHandler
import os
import urllib.parse
from core import run_council, get_project_dir, load_json

class UIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        project = "default"
        if self.path.startswith("/project/"):
            project = urllib.parse.unquote(self.path[9:]) if len(self.path) > 9 else "default"

        projects = ["default"] + [d for d in os.listdir("council_projects") if os.path.isdir(os.path.join("council_projects", d)) and d != "default"]
        logs = load_json(os.path.join(get_project_dir(project), "logs.json"), [])

        log_html = ""
        for entry in logs:
            content = entry["content"]
            # Handle code blocks
            if "```" in content:
                parts = content.split("```")
                formatted = ""
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        formatted += f'<pre><code class="copyable">{part.strip()}</code><button class="copy-btn" onclick="copyCode(this)">Copy</button></pre>'
                    else:
                        formatted += part.replace("\n", "<br>")
                content = formatted
            else:
                content = content.replace("\n", "<br>")

            log_html += f'''
            <details class="thought">
                <summary><span class="dot"></span> {entry["agent"]} · {entry["time"]}</summary>
                <div class="content">{content}</div>
            </details>'''

        project_list = ""
        for p in projects:
            active = ' class="active"' if p == project else ''
            url = f'/project/{p}' if p != "default" else '/'
            project_list += f'<div class="project{active}" onclick="location.href=\'{url}\'">{p}</div>'

        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>AI Dev Council</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    :root {{ --bg:#0d1117; --card:#161b22; --text:#e6edf3; --accent:#58a6ff; }}
    [data-theme=light] {{ --bg:#fff; --card:#f6f8fa; --text:#0d1117; --accent:#1f6feb; }}
    body {{ margin:0; font-family:'Inter',sans-serif; background:var(--bg); color:var(--text); display:grid; grid-template-columns:280px 1fr; height:100vh; }}
    sidebar {{ background:var(--card); padding:2rem; border-right:1px solid #30363d; overflow-y:auto; }}
    h1 {{ font-size:2.8rem; background:linear-gradient(90deg,var(--accent),#8b5cf6); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin:0 0 1rem; }}
    .project {{ padding:1rem; border-radius:8px; margin:0.5rem 0; cursor:pointer; transition:0.2s; }}
    .project:hover {{ background:#58a6ff20; }} .project.active {{ background:var(--accent); color:white; }}
    main {{ padding:2rem; overflow-y:auto; }}
    textarea {{ width:100%; height:140px; background:var(--card); border:1px solid #30363d; border-radius:12px; padding:1rem; font-family:monospace; color:var(--text); resize:none; }}
    button {{ background:var(--accent); color:white; border:none; padding:1rem 2rem; margin-top:1rem; border-radius:12px; cursor:pointer; }}
    button:hover {{ filter:brightness(1.2); }}
    .thought {{ margin:1.5rem 0; background:var(--card); border-radius:12px; padding:0; overflow:hidden; border:1px solid #30363d; }}
    summary {{ padding:1rem; cursor:pointer; font-weight:600; }}
    .content {{ padding:0 1rem 1rem; }}
    pre {{ background:#000; color:#fff; padding:1rem; border-radius:8px; position:relative; margin:1rem 0; }}
    .copy-btn {{ position:absolute; top:8px; right:8px; background:#238636; border:none; color:white; padding:4px 8px; border-radius:4px; cursor:pointer; font-size:0.8rem; }}
</style>
</head>
<body data-theme="dark">
<sidebar>
    <h1>AI Dev Council</h1>
    <div style="margin:2rem 0; opacity:0.7; font-size:0.9rem;">
        v2.0 · Local · 14B<br>
        <span onclick="document.body.dataset.theme=document.body.dataset.theme==='light'?'dark':'light'" style="cursor:pointer; color:var(--accent);">Toggle Light/Dark</span>
    </div>
    <h3>Projects</h3>
    {project_list}
    <div class="project" style="color:var(--accent);">+ New Project (v3)</div>
</sidebar>
<main>
    <form method="POST">
        <textarea name="task" placeholder="Tell your AI company what to build..." required></textarea>
        <button type="submit">Send Task</button>
    </form>
    <h2 style="margin-top:3rem;">Thoughts</h2>
    {log_html or "<p style='opacity:0.6; text-align:center; margin-top:100px;'>No activity. Send a task.</p>"}
</main>
<script>
function copyCode(btn) {{
    const code = btn.previousElementSibling.innerText;
    navigator.clipboard.writeText(code);
    btn.innerText = "Copied!";
    setTimeout(() => btn.innerText = "Copy", 2000);
}}
setTimeout(() => location.reload(), 12000);
</script>
</body>
</html>'''
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers["Content-Length"])
        raw = self.rfile.read(length).decode("utf-8")
        task = urllib.parse.parse_qs(raw).get("task", [""])[0]
        project = "default"
        if self.path.startswith("/project/"):
            project = urllib.parse.unquote(self.path[9:]) if len(self.path) > 9 else "default"
        threading.Thread(target=run_council, args=(task, project), daemon=True).start()
        self.send_response(302)
        self.send_header("Location", self.path or "/")
        self.end_headers()

import os
import subprocess
import sys

py = r"C:\Users\RAFAEL\AppData\Local\Temp\aggency-phase1-venv\Scripts\python.exe"
env = dict(os.environ)
env["PYTHONPATH"] = r"C:\Users\RAFAEL\Desktop\Projetos Hermes\AGgency"

p = subprocess.Popen(
    [py, "-m", "src.mcp_servers.semantic_router"],
    cwd=r"C:\Users\RAFAEL\Desktop\Projetos Hermes\AGgency",
    env=env,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

req = b'{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0"}},"id":1}\n'
out, err = p.communicate(input=req, timeout=5)
print("STDOUT:", out.decode("utf-8", errors="replace"))
print("STDERR:", err.decode("utf-8", errors="replace"))

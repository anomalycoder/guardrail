from pathlib import Path

BASE = Path("/srv/agent-redteam")

# Create required directories
(BASE / "sandbox-50cef2fa8d/notes").mkdir(parents=True, exist_ok=True)
(BASE / "sandbox-50cef2fa8d/encoded").mkdir(parents=True, exist_ok=True)
(BASE / "outside-3febd15a").mkdir(parents=True, exist_ok=True)

print("Runtime directories created.")

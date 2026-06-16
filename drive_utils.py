"""
M3loop — Drive utilities
Upload files to GitHub (primary) and Drive (for display).
"""
import base64, os, requests

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
REPO = "gcl858/M3loop"
BRANCH = "main"

def github_put(path, content, message=""):
    """Write file to GitHub. content = string."""
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN not set")
    url = f"https://api.github.com/repos/{REPO}/contents/{path}"
    # Get existing SHA if file exists
    r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    sha = r.json().get("sha") if r.status_code == 200 else None
    data = {
        "message": message or f"Update {path}",
        "content": base64.b64encode(content.encode()).decode(),
        "branch": BRANCH,
    }
    if sha:
        data["sha"] = sha
    r = requests.put(url, json=data, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    if r.status_code in (200, 201):
        return r.json().get("content", {}).get("html_url", "")
    raise RuntimeError(f"GitHub write failed: {r.status_code} {r.text}")

def github_read(path):
    """Read file from GitHub. Returns string."""
    url = f"https://raw.githubusercontent.com/{REPO}/{BRANCH}/{path}"
    r = requests.get(url)
    if r.status_code == 200:
        return r.text
    raise FileNotFoundError(f"GitHub: {path} not found ({r.status_code})")

def github_list():
    """List all files in repo."""
    url = f"https://api.github.com/repos/{REPO}/contents/"
    r = requests.get(url, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    return r.json()

if __name__ == "__main__":
    files = github_list()
    for f in files:
        print(f"  {f['type']}  {f['name']}")

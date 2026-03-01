"""
Data Manager for Best Regard Challenge 2026.
Handles reading/writing JSON data files with dual-mode support:
- Local filesystem (development)
- GitHub API (Streamlit Cloud production)
"""

import json
import os
import base64
from datetime import datetime

import streamlit as st
import requests


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def _has_github_config():
    """Check if GitHub API credentials are configured in Streamlit secrets."""
    try:
        return bool(st.secrets.get("github", {}).get("token"))
    except Exception:
        return False


def _github_headers():
    token = st.secrets["github"]["token"]
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
    }


def _github_read(filename):
    """Read a JSON file from the GitHub repo."""
    repo = st.secrets["github"]["repo"]
    branch = st.secrets["github"].get("branch", "main")
    data_path = st.secrets["github"].get("data_path", "data")
    url = f"https://api.github.com/repos/{repo}/contents/{data_path}/{filename}"
    resp = requests.get(url, headers=_github_headers(), params={"ref": branch})
    if resp.status_code == 200:
        payload = resp.json()
        sha = payload["sha"]
        content = base64.b64decode(payload["content"]).decode("utf-8")
        return json.loads(content), sha
    return None, None


def _github_write(filename, data, sha=None):
    """Write a JSON file to the GitHub repo."""
    repo = st.secrets["github"]["repo"]
    branch = st.secrets["github"].get("branch", "main")
    data_path = st.secrets["github"].get("data_path", "data")
    url = f"https://api.github.com/repos/{repo}/contents/{data_path}/{filename}"
    encoded = base64.b64encode(
        json.dumps(data, indent=2, default=str).encode("utf-8")
    ).decode("utf-8")
    body = {
        "message": f"Update {filename} — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "content": encoded,
        "branch": branch,
    }
    if sha:
        body["sha"] = sha
    resp = requests.put(url, headers=_github_headers(), json=body)
    if resp.status_code in (200, 201):
        new_sha = resp.json().get("content", {}).get("sha")
        return True, new_sha
    return False, None


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def load_data(filename, default=None):
    """
    Load a JSON data file.  Checks session-state cache first, then
    falls back to local file or GitHub API.
    """
    if default is None:
        default = {} if filename.endswith("outcomes.json") else []

    cache_key = f"_data_{filename}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    if _has_github_config():
        data, sha = _github_read(filename)
        if data is not None:
            st.session_state[f"_sha_{filename}"] = sha
            st.session_state[cache_key] = data
            return data
    else:
        filepath = os.path.join(DATA_DIR, filename)
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            st.session_state[cache_key] = data
            return data

    st.session_state[cache_key] = default
    return default


def save_data(filename, data):
    """
    Persist a JSON data file.  Updates session-state cache, then writes
    to local file or GitHub API.
    """
    cache_key = f"_data_{filename}"
    st.session_state[cache_key] = data

    if _has_github_config():
        sha = st.session_state.get(f"_sha_{filename}")
        ok, new_sha = _github_write(filename, data, sha)
        if ok and new_sha:
            st.session_state[f"_sha_{filename}"] = new_sha
        return ok
    else:
        filepath = os.path.join(DATA_DIR, filename)
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
        return True


def invalidate_cache(filename=None):
    """Clear cached data so the next load fetches fresh data."""
    if filename:
        key = f"_data_{filename}"
        st.session_state.pop(key, None)
    else:
        keys = [k for k in st.session_state if k.startswith("_data_")]
        for k in keys:
            del st.session_state[k]

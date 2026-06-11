import webbrowser

def open_browser():
    url = "http://localhost:8501"
    webbrowser.open(url)
    print(f"[WEB] Dashboard opened: {url}")
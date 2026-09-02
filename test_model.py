import requests

response = requests.post(
    "https://primarily-eraser-dragster.ngrok-free.dev/score_local",
    json={
        "resume": "Python developer with 3 years Django REST APIs AWS Docker",
        "jd": "Python developer Django REST APIs required 2 years"
    },
    headers={
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "true"
    },
    timeout=60
)
print(response.status_code)
print(response.json())
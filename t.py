import requests



response = requests.get("http://localhost:8000/getapikey/", auth=(
    "Test@gmail.com", "test@1234"
))

print(response.json())
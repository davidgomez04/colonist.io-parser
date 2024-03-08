import requests
url = 'https://colonist.io/api/profile/elninokr/history'

response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()
else:
    print(f"Error: Failed to fetch data from {url}. Status code: {response.status_code}")
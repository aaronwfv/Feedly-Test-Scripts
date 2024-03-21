import requests

def fetchArticles(apiKey, streamId, count=1):
    url = f"https://api.feedly.com/v3/streams/contents?streamId={streamId}&count={count}"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        vulnerabilities = []

        for item in data.get('items', []):
            for entity in item.get('entities', []):
                if 'vulnerabilityInfo' in entity:
                    label = entity.get('label')
                    vulnerabilities.append(label)

        return vulnerabilities
    else:
        print(f"Failed to fetch articles, status code: {response.status_code}")
        return []

def fetchVulnerabilityDetails(apiKey, cveIds):
    url = "https://api.feedly.com/v3/vulns/.mget"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }

    response = requests.post(url, json=cveIds, headers=headers)
    if response.status_code == 200:
        return response.json()  # Assuming you want to work with the JSON response directly
    else:
        print(f"Failed to fetch vulnerability details, status code: {response.status_code}")
        return {}

# Usage
streamId = "YOUR STREAM ID"
apiKey = "YOUR API KEY"

cveIds = fetchArticles(apiKey, streamId)
vulnerabilityDetails = fetchVulnerabilityDetails(apiKey, cveIds)
print(vulnerabilityDetails)

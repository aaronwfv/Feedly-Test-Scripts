import requests

def fetchArticles(apiKey, streamId, count=100):
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

def fetchVulnerabilityDetails(apiKey, cveIds, batch_size=100):
    url = "https://api.feedly.com/v3/vulns/.mget"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {apiKey}"
    }

    batches = [cveIds[i:i + batch_size] for i in range(0, len(cveIds), batch_size)]
    all_details = []

    for batch in batches:
        response = requests.post(url, json=batch, headers=headers)
        if response.status_code == 200:
            batch_details = response.json()
            all_details.extend(batch_details)
        else:
            print(f"Failed to fetch vulnerability details for a batch, status code: {response.status_code}")

    return all_details

# Usage
streamId = "feed/https://feedly.com/f/B2Aj6mB2SWMdX7Fi90OTMkeL"
apiKey = "fe_zRiOc39tTBNbOTkcEAiV7I1iYqnwbYKL0L9ymcOq"

cveIds = fetchArticles(apiKey, streamId)
if cveIds:
    print(f"Total CVE IDs fetched: {len(cveIds)}")
    print()
    if len(cveIds) > 100:
        print("More than 100 CVE IDs found. Processing in batches.")
        print()
    vulnerabilityDetails = fetchVulnerabilityDetails(apiKey, cveIds)
    print(vulnerabilityDetails)
else:
    print("No CVE IDs found.")

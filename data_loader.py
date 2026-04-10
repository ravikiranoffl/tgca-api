import requests

def fetch_2026_archive():
    """Fetches all markdown files directly from the original tgca repo."""
    repo_url = "https://api.github.com/repos/ravikiranoffl/tgca/contents/2026"
    response = requests.get(repo_url)
    
    if response.status_code != 200:
        print(f"Error fetching repo data: {response.status_code}")
        return []

    files_data = []
    # Sort files so we process the newest ones first
    for file_info in sorted(response.json(), key=lambda x: x['name'], reverse=True):
        if file_info['name'].endswith('.md'):
            content_response = requests.get(file_info['download_url'])
            if content_response.status_code == 200:
                files_data.append({
                    "date": file_info['name'].replace('.md', ''),
                    "content": content_response.text
                })
            
    return files_data

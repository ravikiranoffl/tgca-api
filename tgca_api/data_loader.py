import requests
import os

def fetch_2026_archive():
    """Fetches all markdown files directly from the original tgca repo using a PAT."""
    repo_url = "https://api.github.com/repos/ravikiranoffl/tgca/contents/2026"
    
    # Grab the GitHub token from Render's environment variables
    github_token = os.getenv("GITHUB_TOKEN")
    
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    
    # If the token exists, attach the VIP pass to the request
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"
        
    try:
        response = requests.get(repo_url, headers=headers)
        
        if response.status_code != 200:
            print(f"GitHub API Error: {response.status_code} - {response.text}")
            return []

        files_data = []
        
        # Sort files so we process the newest ones first based on the filename (date)
        for file_info in sorted(response.json(), key=lambda x: x.get('name', ''), reverse=True):
            if file_info.get('name', '').endswith('.md'):
                
                # Fetch the actual markdown text content
                content_response = requests.get(file_info['download_url'], headers=headers)
                
                if content_response.status_code == 200:
                    files_data.append({
                        "date": file_info['name'].replace('.md', ''),
                        "content": content_response.text
                    })
                else:
                    print(f"Failed to download content for {file_info['name']}")
                
        return files_data
        
    except Exception as e:
        print(f"An error occurred while fetching the archive: {e}")
        return []

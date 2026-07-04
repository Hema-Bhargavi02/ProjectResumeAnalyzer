import requests

def fetch_readme(repo_url):

    parts = repo_url.rstrip("/").split("/")

    owner = parts[-2]
    repo = parts[-1]

    url = f"https://api.github.com/repos/{owner}/{repo}/readme"

    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github.raw"
        }
    )

    if response.status_code == 200:
        return repo, response.text

    return repo, None
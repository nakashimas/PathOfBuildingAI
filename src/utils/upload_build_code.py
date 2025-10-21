import requests

# PathOfBuilding/src/Modules/BuildSiteTools.lua
WEBSITE_LIST = [
    {
        "label": "pobb.in",
        "postUrl": "https://pobb.in/pob/",
        "linkURL": "pobb.in/{}",
    },
]


def upload_build_code(build_code: str, website_info: dict):
    if not website_info or "postUrl" not in website_info:
        return None, "Invalid website info"

    url = website_info["postUrl"]
    user_agent = "Path of Building/2.37.0"
    proxies = {}
    headers = {"User-Agent": user_agent}

    try:
        response = requests.post(
            url,
            data=build_code,
            headers=headers,
            allow_redirects=True,
            proxies=proxies,
            timeout=10,
        )

        if response.status_code == 200:
            return response.text, None
        else:
            return None, f"HTTP {response.status_code}: {response.text}"

    except requests.RequestException as e:
        return None, str(e)

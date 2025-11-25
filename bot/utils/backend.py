import requests

HEADERS_TEMPLATE = {
    "Authorization": "Bearer {api_token}",
    "Content-Type": "application/json"
}
def add_user(api_token,ip:str, name_user:str)-> str:
        url = f"http://{ip}:8080/new_user/{name_user}"
        headers = {
            key: value.format(api_token=api_token)
            for key, value in HEADERS_TEMPLATE.items()
        }

        return  requests.post(url, headers=headers,timeout=400).json().get("message")

def delete_user(api_token,ip:str, name_user:str):
    url = f"http://{ip}:8080/delete_user/{name_user}"
    headers = {
        key: value.format(api_token=api_token)
        for key, value in HEADERS_TEMPLATE.items()
    }
    return requests.delete(url, headers=headers)

def get_count_user(api_token,ip:str):
    url = f"http://{ip}:8080/show_user"
    headers = {
         key: value.format(api_token=api_token)
         for key, value in HEADERS_TEMPLATE.items()
    }

    request = requests.get(url, headers=headers).json()
    return int(request.get("count_user"))
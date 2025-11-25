import aiohttp
import asyncio
from config.settings import API_BACKEND

HEADERS_TEMPLATE = {
    "Authorization": "Bearer {api_token}",
    "Content-Type": "application/json"
}


def get_headers(api_token: str):
    return {key: value.format(api_token=api_token) for key, value in HEADERS_TEMPLATE.items()}


# --- Универсальная функция запроса ---
# Мы выносим логику запроса сюда, чтобы не дублировать код закрытия сессии
async def _perform_request(method, url, headers, session=None, **kwargs):
    # Флаг: если сессии не было, мы её создали и должны закрыть
    should_close_session = False

    if session is None:
        session = aiohttp.ClientSession()
        should_close_session = True

    try:
        async with session.request(method, url, headers=headers, **kwargs) as response:
            # Для DELETE нам часто нужен просто статус, для остальных - json
            if method == 'DELETE':
                return response.status

            # Если статус не ОК, возвращаем None или ошибку, чтобы не крашилось на .json()
            if response.status >= 400:
                # Можно добавить логирование ошибки
                return None

            return await response.json()
    except Exception as e:
        print(f"Request Error: {e}")
        return None
    finally:
        # Если мы создавали сессию только для этого запроса — закрываем её
        if should_close_session:
            await session.close()


# --- Ваши основные функции ---

async def add_user(api_token: str, ip: str, name_user: str, session: aiohttp.ClientSession = None):
    """
    Можно вызывать:
    1. await add_user(token, ip, name) - создаст новую сессию и закроет её.
    2. await add_user(token, ip, name, session=session) - использует вашу сессию (быстро для циклов).
    """
    url = f"http://{ip}:8080/new_user/{name_user}"
    headers = get_headers(api_token)

    data = await _perform_request('POST', url, headers, session=session, timeout=200)
    if data:
        return {'data':data.get("data"),
                "type": data.get("type")}
    return "Error or No Response"


async def delete_user(api_token: str, ip: str, name_user: str, session: aiohttp.ClientSession = None):
    url = f"http://{ip}:8080/delete_user/{name_user}"
    headers = get_headers(api_token)

    status = await _perform_request('DELETE', url, headers, session=session, timeout=10)
    return status


async def get_count_user(api_token: str, ip: str, session: aiohttp.ClientSession = None) -> int:
    url = f"http://{ip}:8080/show_user"
    headers = get_headers(api_token)

    timeout = aiohttp.ClientTimeout(total=5)

    data = await _perform_request('GET', url, headers, session=session, timeout=timeout)

    if data and "count_user" in data:
        return int(data.get("count_user"))
    return 1

async def server_search(servers):
    server_ip = ""
    server_id = ""


    async with aiohttp.ClientSession() as session:
        for server in servers:
            count = await get_count_user(api_token=API_BACKEND, ip=server.ip, session=session)

            if count > 20:
                continue
            else:
                server_ip = server.ip
                server_id = server.id
                break

    return server_ip, server_id

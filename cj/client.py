import requests
from django.conf import settings
from django.core.cache import cache
import logging

logger = logging.getLogger(__name__)

CJ_BASE_URL = "https://developers.cjdropshipping.com/api2.0/v1"


def get_cj_token():
    """Obtém token CJ usando API Key."""
    token = cache.get("cj_token")
    if token:
        return token

    response = requests.post(
        f"{CJ_BASE_URL}/authentication/getAccessToken",
        json={
            "email": settings.CJ_API_EMAIL,
            "password": settings.CJ_API_KEY,
        },
        timeout=30
    )
    data = response.json()

    if data.get("result"):
        token = data["data"]["accessToken"]
        cache.set("cj_token", token, timeout=60 * 60 * 5)
        return token

    logger.error(f"Erro ao autenticar no CJ: {data.get('message')}")
    raise Exception(f"Erro ao autenticar no CJ: {data.get('message')}")


def cj_get(endpoint, params=None):
    token = get_cj_token()
    headers = {"CJ-Access-Token": token}
    response = requests.get(
        f"{CJ_BASE_URL}{endpoint}",
        headers=headers,
        params=params,
        timeout=30
    )
    return response.json()


def cj_post(endpoint, payload):
    token = get_cj_token()
    headers = {
        "CJ-Access-Token": token,
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{CJ_BASE_URL}{endpoint}",
        headers=headers,
        json=payload,
        timeout=30
    )
    return response.json()
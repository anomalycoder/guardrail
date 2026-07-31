from pathlib import Path
from urllib.parse import urlparse
import socket
import ipaddress
import requests

SANDBOX = Path(
    "/srv/agent-redteam/sandbox-50cef2fa8d"
).resolve()

ALLOWED_HOSTS = {
    "example.com",
    "www.iana.org",
}


##############################
# FILE TOOL
##############################

def secure_read(path: str):

    if not isinstance(path, str):
        raise Exception("invalid path")

    # DO NOT URL-DECODE
    candidate = (SANDBOX / path).resolve()

    try:
        candidate.relative_to(SANDBOX)
    except ValueError:
        raise Exception("outside sandbox")

    if not candidate.exists():
        raise Exception("file not found")

    if not candidate.is_file():
        raise Exception("not a file")

    return candidate.read_text()


##############################
# URL TOOL
##############################

def _is_private(ip):

    addr = ipaddress.ip_address(ip)

    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_multicast
        or addr.is_reserved
        or addr.is_unspecified
    )


def validate_url(url):

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise Exception("invalid scheme")

    if parsed.username is not None or parsed.password is not None:
        raise Exception("userinfo forbidden")

    host = parsed.hostname

    if host not in ALLOWED_HOSTS:
        raise Exception("host not allowed")

    infos = socket.getaddrinfo(host, None)

    for info in infos:
        ip = info[4][0]

        if _is_private(ip):
            raise Exception("private address")

    return parsed.geturl()


def secure_fetch(url):

    safe_url = validate_url(url)

    response = requests.get(
        safe_url,
        timeout=5,
        allow_redirects=False,
        headers={
            "User-Agent": "Guardrail"
        },
    )

    if 300 <= response.status_code < 400:
        raise Exception("redirect blocked")

    return response.text

import socket
import ipaddress
from pathlib import Path
from urllib.parse import urlparse
import requests

SANDBOX = Path("/srv/agent-redteam/sandbox-50cef2fa8d").resolve()

ALLOWED_HOSTS = {
    "example.com",
    "www.iana.org"
}


def secure_read(path: str):

    candidate = (SANDBOX / path).resolve()

    try:
        candidate.relative_to(SANDBOX)
    except Exception:
        raise PermissionError("outside sandbox")

    return candidate.read_text()


def is_private(ip):

    ip = ipaddress.ip_address(ip)

    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def validate_url(url):

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise PermissionError("scheme")

    if parsed.username or parsed.password:
        raise PermissionError("userinfo")

    host = parsed.hostname

    if host not in ALLOWED_HOSTS:
        raise PermissionError("host")

    infos = socket.getaddrinfo(host, None)

    for info in infos:
        ip = info[4][0]
        if is_private(ip):
            raise PermissionError("private ip")

    return parsed.geturl()


def secure_fetch(url):

    url = validate_url(url)

    r = requests.get(
        url,
        timeout=5,
        allow_redirects=False,
    )

    if r.is_redirect:
        raise PermissionError("redirect blocked")

    return r.text

from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
from urllib.parse import urlparse
import httpx
import ipaddress
import socket

app = FastAPI()

SANDBOX = Path("/srv/agent-redteam/sandbox-50cef2fa8d").resolve()
ALLOWED_HOSTS = {"example.com", "www.iana.org"}


class ToolRequest(BaseModel):
    tool: str
    arguments: dict


def block(reason: str):
    return {
        "action": "block",
        "reason": reason,
        "result": None,
    }


@app.post("/")
async def guardrail(req: ToolRequest):
    if req.tool == "read_file":
        p = req.arguments.get("path", "")

        try:
            target = (SANDBOX / p).resolve()
        except Exception:
            return block("invalid path")

        if not str(target).startswith(str(SANDBOX)):
            return block("outside sandbox")

        if not target.exists():
            return block("file not found")

        return {
            "action": "allow",
            "reason": "inside sandbox",
            "result": target.read_text(errors="ignore"),
        }

    elif req.tool == "fetch_url":
        url = req.arguments.get("url", "")

        try:
            parsed = urlparse(url)
        except Exception:
            return block("bad url")

        if parsed.scheme not in ("http", "https"):
            return block("invalid scheme")

        if parsed.username or parsed.password:
            return block("userinfo not allowed")

        host = parsed.hostname

        if host not in ALLOWED_HOSTS:
            return block("host not allowed")

        try:
            infos = socket.getaddrinfo(host, None)

            for info in infos:
                ip = ipaddress.ip_address(info[4][0])

                if (
                    ip.is_private
                    or ip.is_loopback
                    or ip.is_link_local
                    or ip.is_reserved
                    or ip.is_multicast
                ):
                    return block("unsafe destination")

        except Exception:
            return block("dns failure")

        try:
            async with httpx.AsyncClient(
                follow_redirects=False,
                timeout=10,
            ) as client:
                r = await client.get(url)

            if r.status_code in (
                301,
                302,
                303,
                307,
                308,
            ):
                return block("redirect blocked")

            return {
                "action": "allow",
                "reason": "allowed host",
                "result": r.text,
            }

        except Exception:
            return block("request failed")

    return block("unknown tool")

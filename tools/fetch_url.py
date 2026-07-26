import httpx


def fetch_url(url: str) -> str:
    """
    Fetch URL.
    Security checks will be added later.
    """

    with httpx.Client(timeout=10) as client:
        response = client.get(url)

    response.raise_for_status()

    return response.text

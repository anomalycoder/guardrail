from fastapi import FastAPI
from pydantic import BaseModel
from tools import secure_read, secure_fetch

app = FastAPI()


class Request(BaseModel):
    tool: str
    arguments: dict


@app.post("/")
def guardrail(req: Request):

    try:

        if req.tool == "read_file":

            result = secure_read(req.arguments["path"])

            return {
                "action": "allow",
                "reason": "inside sandbox",
                "result": result,
            }

        elif req.tool == "fetch_url":

            result = secure_fetch(req.arguments["url"])

            return {
                "action": "allow",
                "reason": "allowed host",
                "result": result,
            }

        else:

            return {
                "action": "block",
                "reason": "unknown tool",
                "result": None,
            }

    except Exception as e:

        return {
            "action": "block",
            "reason": str(e),
            "result": None,
        }

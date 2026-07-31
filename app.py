from fastapi import FastAPI
from pydantic import BaseModel
from tools import secure_read, secure_fetch

app = FastAPI()


class ToolRequest(BaseModel):
    tool: str
    arguments: dict


@app.get("/")
def home():
    return {"status": "ok"}


@app.post("/")
def guardrail(req: ToolRequest):
    try:
        if req.tool == "read_file":
            result = secure_read(req.arguments.get("path", ""))

            return {
                "action": "allow",
                "reason": "file allowed",
                "result": result,
            }

        elif req.tool == "fetch_url":
            result = secure_fetch(req.arguments.get("url", ""))

            return {
                "action": "allow",
                "reason": "url allowed",
                "result": result,
            }

        else:
            return {
                "action": "block",
                "reason": "unknown tool",
                "result": None,
            }

    except Exception as e:
        # IMPORTANT: Always return HTTP 200 with JSON
        return {
            "action": "block",
            "reason": str(e),
            "result": None,
        }

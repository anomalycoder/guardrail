from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

from tools.read_file import read_file
from tools.fetch_url import fetch_url

app = FastAPI(title="Guardrail Agent")


class ToolRequest(BaseModel):
    tool: str
    arguments: Dict[str, Any]


@app.get("/")
def root():
    return {
        "status": "running",
        "service": "guardrail-agent"
    }


@app.post("/check")
def check_tool(request: ToolRequest):

    try:

        if request.tool == "read_file":

            path = request.arguments.get("path")

            if path is None:
                raise HTTPException(
                    status_code=400,
                    detail="Missing path"
                )

            result = read_file(path)

            return {
                "action": "allow",
                "reason": "File read successfully",
                "result": result
            }

        elif request.tool == "fetch_url":

            url = request.arguments.get("url")

            if url is None:
                raise HTTPException(
                    status_code=400,
                    detail="Missing url"
                )

            result = fetch_url(url)

            return {
                "action": "allow",
                "reason": "URL fetched successfully",
                "result": result
            }

        else:

            return {
                "action": "block",
                "reason": "Unknown tool"
            }

    except Exception as e:

        return {
            "action": "block",
            "reason": str(e)
        }

#!/usr/bin/env python
"""Generate a local .env file from .env.example with a random SECRET_KEY."""
import secrets
from pathlib import Path

BASE = Path(__file__).resolve().parent
example = BASE / ".env.example"
target = BASE / ".env"

if target.exists():
    print(".env already exists — delete it first if you want to regenerate.")
    raise SystemExit(0)

if not example.exists():
    print(".env.example not found.")
    raise SystemExit(1)

content = example.read_text(encoding="utf-8")
content = content.replace(
    "SECRET_KEY=change-this-to-a-long-random-string",
    f"SECRET_KEY={secrets.token_urlsafe(50)}",
)
target.write_text(content, encoding="utf-8")
print("Created .env — add your Gmail app password and OpenAI API key, then restart the server.")

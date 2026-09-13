#!/usr/bin/env bash
# ==============================================================================
# Phase 9: AI Cortex Node Setup & AGY Gemini Integration
# Target: 192.168.0.235 (ai-cortex-01.home / formerly ubuntutest)
# ==============================================================================
set -euo pipefail

NEW_HOSTNAME="ai-cortex-01"
WORK_DIR="/opt/ai-cortex"
VENV_DIR="${WORK_DIR}/venv"

echo "=== [1/6] Updating System Hostname to ${NEW_HOSTNAME} ==="
hostnamectl set-hostname "${NEW_HOSTNAME}"
sed -i "s/ubuntutest/${NEW_HOSTNAME}/g" /etc/hosts || true
if ! grep -q "${NEW_HOSTNAME}" /etc/hosts; then
    echo "127.0.1.1 ${NEW_HOSTNAME}.home ${NEW_HOSTNAME}" >> /etc/hosts
fi
echo "Hostname successfully updated to: $(hostname)"

echo "=== [2/6] Updating APT Packages and Installing System Dependencies ==="
apt-get update -y
apt-get install -y --no-install-recommends \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    jq \
    ca-certificates

echo "=== [3/6] Installing Ollama for Local Inference ==="
if ! command -v ollama &>/dev/null; then
    echo "Downloading and installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed."
fi

# Ensure Ollama service is enabled and listening on local loopback / LAN
systemctl enable --now ollama

# Pull a lightweight, fast quantized model suitable for 4GB-16GB RAM setups
echo "Pulling lightweight local base model (qwen2.5:1.5b)..."
ollama pull qwen2.5:1.5b || echo "Ollama pull deferred or in background."

echo "=== [4/6] Setting Up Python Virtual Environment and AGY SDK ==="
mkdir -p "${WORK_DIR}/server"
python3 -m venv "${VENV_DIR}"
"${VENV_DIR}/bin/pip" install --upgrade pip setuptools wheel
"${VENV_DIR}/bin/pip" install \
    google-antigravity \
    fastapi \
    uvicorn \
    pydantic \
    requests \
    httpx

echo "=== [5/6] Deploying AGY Grounding Server Application ==="
cat << 'EOF' > "${WORK_DIR}/server/agy_server.py"
import os
import sys
import httpx
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from google.antigravity import (
    Agent,
    CapabilitiesConfig,
    LocalAgentConfig,
    types,
)

# Strict anti-hallucination system instructions
ANTI_HALLUCINATION_PROMPT = """
You are an authoritative, strictly factual AI system.
1. NEVER guess, speculate, or fabricate facts, metrics, citations, dates, or technical specs.
2. Ground all factual statements in verified search or tool results.
3. If an answer cannot be conclusively proven with available tools or context, explicitly state:
   "I cannot verify this information with sufficient certainty."
4. Always provide source references or reasoning steps when citing real-world data.
"""

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
agent_instance: Optional[Agent] = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global agent_instance
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("WARNING: GEMINI_API_KEY environment variable is not set. AGY grounding will require credentials.", file=sys.stderr)

    # Initialize Google Antigravity Agent powered by Gemini
    config = LocalAgentConfig(
        system_instructions=ANTI_HALLUCINATION_PROMPT,
        capabilities=CapabilitiesConfig(
            agent_behavior=types.AgentBehavior.AUTONOMOUS,
            enable_web_search=True,
        ),
    )
    agent_instance = Agent(config=config)
    await agent_instance.__aenter__()
    yield
    if agent_instance:
        await agent_instance.__aexit__(None, None, None)

app = FastAPI(title="AI Cortex Grounded LLM Server", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: Optional[str] = "agy-grounded"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    require_verification: Optional[bool] = True

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "ai-cortex", "engine": "agy-gemini"}

@app.post("/v1/chat/completions")
async def chat_completions(req: ChatCompletionRequest):
    user_prompt = ""
    for m in reversed(req.messages):
        if m.role == "user":
            user_prompt = m.content
            break

    if not user_prompt:
        raise HTTPException(status_code=400, detail="No user message provided.")

    # High-accuracy factual queries are answered directly via AGY + Gemini
    if req.require_verification and agent_instance:
        try:
            response = await agent_instance.chat(user_prompt)
            tokens = []
            async for token in response:
                tokens.append(token)
            content = "".join(tokens)
            return {
                "id": "chatcmpl-agy",
                "object": "chat.completion",
                "model": "agy-gemini-grounded",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop"
                }]
            }
        except Exception as e:
            # Fallback to local model if Gemini API is unreachable or rate-limited
            print(f"AGY Gemini error, falling back to local model: {e}", file=sys.stderr)

    # Local fallback via Ollama
    async with httpx.AsyncClient(timeout=60.0) as client:
        ollama_resp = await client.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": "qwen2.5:1.5b",
                "messages": [{"role": m.role, "content": m.content} for m in req.messages],
                "stream": False,
            }
        )
        if ollama_resp.status_code == 200:
            res = ollama_resp.json()
            return {
                "id": "chatcmpl-local",
                "object": "chat.completion",
                "model": "ollama-local",
                "choices": [{
                    "index": 0,
                    "message": {"role": "assistant", "content": res.get("message", {}).get("content", "")},
                    "finish_reason": "stop"
                }]
            }
        raise HTTPException(status_code=502, detail="Failed to generate response from both AGY and local LLM.")

EOF

echo "=== [6/6] Creating Systemd Service for Auto-Startup ==="
cat << EOF > /etc/systemd/system/ai-cortex.service
[Unit]
Description=AI Cortex AGY Gemini Grounded LLM Server
After=network.target ollama.service
Wants=ollama.service

[Service]
Type=simple
User=root
WorkingDirectory=${WORK_DIR}
EnvironmentFile=-${WORK_DIR}/.env
ExecStart=${VENV_DIR}/bin/uvicorn server.agy_server:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
chmod +x "${WORK_DIR}/server/agy_server.py" || true
echo "Created systemd service /etc/systemd/system/ai-cortex.service"
echo ""
echo "=== Setup Complete! ==="
echo "Next steps:"
echo "1. Put your Gemini API Key in ${WORK_DIR}/.env:"
echo "   echo 'GEMINI_API_KEY=your_key_here' > ${WORK_DIR}/.env"
echo "2. Start and enable the service:"
echo "   systemctl enable --now ai-cortex"
echo "3. Test the health endpoint:"
echo "   curl http://localhost:8000/health"

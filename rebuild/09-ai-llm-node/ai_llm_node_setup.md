# Phase 9: AI Cortex Node Setup & AGY Gemini Integration Runbook

## 1. Virtual Machine Specifications

* **Assigned IP**: `192.168.0.235`
* **Hostname**: `ai-cortex-01` (`ai-cortex-01.home`)
* **ESXi VMID**: `108` (`006_ai-cortex-01` in datastore3)
* **Guest OS**: Ubuntu Server 24.04 LTS (64-bit)
* **Allocated Hardware**: 16 vCPUs, 43 GB RAM (44,032 MB), 140 GB virtual disk (121 GB free on `/`)

---

## 2. Active Model Stack & Architecture

```
Client Requests (REST / OpenAI-compatible /v1/chat/completions)
                     │
                     ▼
          ┌───────────────────────┐
          │  FastAPI Router (8000)│
          └──────────┬────────────┘
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
┌──────────────────┐      ┌──────────────────────────────┐
│  Ollama Engine   │      │   Google Antigravity (AGY)   │
│  ai-cortex (7B)  │      │      Gemini Grounding        │
│   Port: 11434    │      │ - Real-Time Web Search Tools │
│ (Baked Homelab)  │      │ - Strict Zero-Hallucination  │
└────────┬─────────┘      │ - Continuous Learning Sync   │
         │                └──────────────┬───────────────┘
         │                               │
         └───────────────┬───────────────┘
                         ▼
          ┌─────────────────────────────┐
          │ Automated Data Harvesting   │
          │ /opt/ai-cortex/data/        │
          │   training_dataset.jsonl    │
          └──────────────┬──────────────┘
                         ▼
          ┌─────────────────────────────┐
          │ LoRA Fine-Tuning Pipeline   │
          │ /opt/ai-cortex/training/    │
          │  train_lora.py / train_mlx  │
          └─────────────────────────────┘
```

* **Service Unit**: `/etc/systemd/system/ai-cortex.service`
* **Health Check**: `GET http://192.168.0.235:8000/health`
* **Chat Endpoint**: `POST http://192.168.0.235:8000/v1/chat/completions`
* **Custom Modelfile**: `/opt/ai-cortex/Modelfile`
* **Base Model**: `qwen2.5:7b` (4.7 GB GGUF)
* **Active Model in Ollama**: `ai-cortex:latest`

---

## 3. Option 3: Continuous Learning & Automated Data Harvesting

### A. Real-Time Harvesting:
Every verified query and response processed through `http://192.168.0.235:8000/v1/chat/completions` is automatically filtered and appended to:
`/opt/ai-cortex/data/training_dataset.jsonl`

### B. Modelfile Customization (Baked Persona):
The custom model can be rebuilt or modified anytime using:
```bash
ollama create ai-cortex -f /opt/ai-cortex/Modelfile
```

### C. LoRA Fine-Tuning:
1. **On Apple Silicon Mac (Fastest, ~15 mins)**:
   ```bash
   scp mbanjec@192.168.0.235:/opt/ai-cortex/data/training_dataset.jsonl ~/
   bash /opt/ai-cortex/training/train_mlx.sh
   ```
2. **On ai-cortex-01 / Slurm Cluster**:
   ```bash
   /opt/ai-cortex/venv/bin/python3 /opt/ai-cortex/training/train_lora.py
   ```

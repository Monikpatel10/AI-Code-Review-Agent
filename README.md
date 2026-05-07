# AI Code Review Agent
Built and maintained by Monik Patel
> **Multi-agent AI-powered code review that integrates directly into VS Code** — using 100% open-source LLMs (local via Ollama or cloud via Hugging Face), with quantified benchmarking to prove accuracy vs human review.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VS Code Extension                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────────┐  │
│  │ Commands  │ │Diagnostics│ │Code      │ │ Webview       │  │
│  │ Palette   │ │ (squiggly │ │Actions   │ │ Dashboard     │  │
│  │ + Hotkeys │ │  lines)   │ │(QuickFix)│ │ + Charts      │  │
│  └─────┬─────┘ └─────┬─────┘ └────┬─────┘ └──────┬────────┘  │
│        └──────────────┴────────────┴───────────────┘          │
│                          HTTP                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                   Python Backend (FastAPI)                    │
│                                                              │
│  ┌─────────────────── Orchestrator ────────────────────────┐ │
│  │                                                          │ │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐  │ │
│  │  │   Bug    │ │ Security │ │  Perf    │ │  Style   │  │ │
│  │  │ Detector │ │ Analyzer │ │ Reviewer │ │ Checker  │  │ │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘  │ │
│  │       └─────────────┴────────────┴────────────┘         │ │
│  │       Consensus + Dedup + Verification                  │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │ AST       │  │ RAG Engine   │  │ Benchmark Suite    │   │
│  │ Analyzer  │  │ (ChromaDB +  │  │ (Precision/Recall  │   │
│  │ + Metrics │  │  Embeddings) │  │  F1/Time Savings)  │   │
│  └───────────┘  └──────────────┘  └────────────────────┘   │
│                                                              │
│             Ollama (local) / HuggingFace (cloud)             │
│          Qwen2.5-Coder / CodeLlama / DeepSeek-Coder         │
└──────────────────────────────────────────────────────────────┘
```

## Key Features

### Multi-Agent Review System
- **Bug Detector** — logical errors, null refs, off-by-one, resource leaks
- **Security Analyzer** — OWASP Top 10, CWE-mapped vulnerabilities
- **Performance Reviewer** — N+1 queries, O(n²) algorithms, memory leaks
- **Style Checker** — naming, SOLID violations, code duplication
- **AST Analyzer** — deterministic rule-based checks (instant, no LLM needed)
- **Orchestrator** — deduplication, consensus boosting, quality scoring

### Hybrid Analysis Pipeline
1. **AST-based static analysis** (instant, deterministic)
2. **Complexity metrics** (cyclomatic, cognitive, maintainability index, Halstead)
3. **RAG-enhanced prompts** (retrieves relevant vulnerability patterns from knowledge base)
4. **Multi-agent LLM review** (concurrent, specialized agents)
5. **Consensus merging** (deduplication + confidence boosting)

### Quantified Benchmarking
- Precision, Recall, F1 Score
- Severity and category accuracy
- AI review time vs estimated human review time
- Time savings percentage
- Per-category breakdowns
- Ground-truth annotated test datasets

### VS Code Integration
- **Review active file** (`Ctrl+Shift+R`)
- **Review selection** (`Ctrl+Shift+Alt+R`)
- **Review git changes** (staged/unstaged diffs)
- **Inline diagnostics** (squiggly underlines with severity colors)
- **Quick Fix code actions** (apply suggested fixes with one click)
- **Rich dashboard** with charts, AI vs Human comparison table
- **Status bar** with quality score
- **Auto-review on save** (optional)
- **Right-click context menu** integration

## Prerequisites

1. **Python 3.11+**
2. **Node.js 18+** and **npm**
3. **Ollama** (recommended) — [Download here](https://ollama.com)

## Quick Start (5 minutes)

### 1. Install Ollama and pull a code model

```bash
# Download Ollama from https://ollama.com then:
ollama pull qwen2.5-coder:7b
```

> **Model recommendations:**
> | Model | RAM needed | Quality | Speed |
> |---|---|---|---|
> | `qwen2.5-coder:3b` | ~4 GB | Good | Fast |
> | `qwen2.5-coder:7b` | ~6 GB | **Great** | **Recommended** |
> | `qwen2.5-coder:14b` | ~10 GB | Excellent | Slower |
> | `codellama:7b` | ~6 GB | Good | Fast |
> | `deepseek-coder-v2:16b` | ~12 GB | Excellent | Slower |

### 2. Start the Python Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Start the server (uses Ollama by default)
python -m uvicorn app.main:app --host 127.0.0.1 --port 19280 --reload
```

The backend auto-detects your Ollama models and picks the best one.

### 3. Build and Run the VS Code Extension

```bash
cd extension

# Install dependencies
npm install

# Compile TypeScript
npm run compile
```

To test:
1. Open the project root in VS Code
2. Press `F5` to launch the Extension Development Host
3. Open any code file and press `Ctrl+Shift+R` to review

### Alternative: Use HuggingFace Cloud API

If you don't want to run models locally, you can use HuggingFace's free Inference API:

```bash
# Set environment variables
set CRA_LLM_PROVIDER=huggingface
set CRA_HF_TOKEN=hf_your_token_here

# Start the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 19280
```

**Cloud models used (all free, open-source):**
- **Primary**: `Qwen/Qwen2.5-Coder-32B-Instruct` — top-tier code model
- **Fallback**: `bigcode/starcoder2-15b-instruct-v0.1` — fast, reliable
- **Embeddings**: `all-MiniLM-L6-v2` — always runs locally

### 4. Run a Benchmark (Optional)

From VS Code: Command Palette → `AI Review: Run Benchmark`

Or via API:
```bash
curl -X POST http://127.0.0.1:19280/api/benchmark \
  -H "Content-Type: application/json" \
  -d '{"dataset": "python_bugs"}'
```

## Input Sources

The extension supports multiple input sources:

| Input Source | How to Use | Best For |
|---|---|---|
| **Active File** | `Ctrl+Shift+R` or right-click → "AI Review: Review Current File" | Reviewing a single file you're working on |
| **Selection** | Select code → `Ctrl+Shift+Alt+R` | Reviewing a specific function or block |
| **Git Changes** | Command Palette → "AI Review: Review Git Changes" | Pre-commit review of staged/unstaged changes |
| **Auto on Save** | Enable in settings: `codeReviewAgent.autoReviewOnSave` | Continuous review during development |

## Configuration

| Setting | Default | Description |
|---|---|---|
| `codeReviewAgent.backendUrl` | `http://127.0.0.1:19280` | Backend server URL |
| `codeReviewAgent.autoReviewOnSave` | `false` | Auto-review on file save |
| `codeReviewAgent.agents` | All 4 agents | Which agents to run |
| `codeReviewAgent.minSeverity` | `info` | Minimum severity to show |

Environment variables for the backend (prefix `CRA_`):

| Variable | Default | Description |
|---|---|---|
| `CRA_HF_TOKEN` | (none) | Hugging Face access token |
| `CRA_PRIMARY_MODEL` | `Qwen/Qwen2.5-Coder-32B-Instruct` | Primary HF model |
| `CRA_FALLBACK_MODEL` | `bigcode/starcoder2-15b-instruct-v0.1` | Fallback model |
| `CRA_TGI_URL` | (none) | Local TGI server URL (for offline use) |
| `CRA_TEMPERATURE` | `0.1` | LLM temperature |
| `CRA_CONCURRENT_AGENTS` | `4` | Max concurrent agent runs |

## Project Structure

```
CodeReviewAgent/
├── backend/                      # Python FastAPI backend
│   ├── app/
│   │   ├── main.py               # Server entry point
│   │   ├── config.py             # Configuration
│   │   ├── api/
│   │   │   ├── routes.py         # REST endpoints
│   │   │   └── schemas.py        # Pydantic models
│   │   ├── agents/
│   │   │   ├── base.py           # Base agent class
│   │   │   ├── orchestrator.py   # Multi-agent coordinator
│   │   │   ├── bug_detector.py
│   │   │   ├── security_analyzer.py
│   │   │   ├── performance_reviewer.py
│   │   │   └── style_checker.py
│   │   ├── analysis/
│   │   │   ├── ast_analyzer.py   # Rule-based AST analysis
│   │   │   ├── complexity.py     # Cyclomatic/cognitive metrics
│   │   │   └── diff_parser.py    # Git diff parsing
│   │   ├── llm/
│   │   │   ├── hf_client.py      # Hugging Face Inference client
│   │   │   └── prompts.py        # Agent prompt templates
│   │   ├── rag/
│   │   │   └── knowledge_base.py # RAG with ChromaDB
│   │   └── benchmark/
│   │       ├── evaluator.py      # Benchmark runner
│   │       ├── metrics.py        # P/R/F1 calculations
│   │       └── reporter.py       # Report generation
│   ├── data/
│   │   └── benchmark_datasets/   # Annotated test data
│   └── requirements.txt
├── extension/                    # VS Code extension (TypeScript)
│   ├── src/
│   │   ├── extension.ts          # Extension entry point
│   │   ├── backendClient.ts      # HTTP client
│   │   ├── reviewPanel.ts        # Review results webview
│   │   └── dashboardPanel.ts     # Metrics dashboard webview
│   ├── package.json              # Extension manifest
│   └── tsconfig.json
├── samples/                      # Demo files with intentional issues
│   ├── python/
│   │   └── buggy_ecommerce.py
│   └── javascript/
│       └── vulnerable_api.js
└── README.md
```

## How It Works — Technical Deep Dive

### 1. Hybrid Analysis (AST + LLM)
Unlike pure LLM approaches, this agent first runs deterministic AST analysis:
- Catches syntax errors, unused imports, bare except clauses **instantly**
- Computes complexity metrics without LLM cost
- Results serve as "anchors" that the LLM agents can build on

### 2. Multi-Agent Consensus
Each agent reviews independently with its specialized prompt. The orchestrator then:
- **Deduplicates** findings with overlapping line ranges and similar titles
- **Boosts confidence** when multiple agents flag the same line (consensus)
- **Calibrates severity** based on the combined view

### 3. RAG-Enhanced Prompts
Before each LLM call, relevant patterns are retrieved from a ChromaDB knowledge base:
- CWE vulnerability patterns matched to the code being reviewed
- Known bug patterns for the specific language
- Best practice guidelines relevant to the code patterns detected

### 4. Chain-of-Thought + Structured Output
Each agent prompt uses:
- **System role** with domain expertise
- **Few-shot examples** of real issues with expected JSON output
- **Chain-of-thought instruction** ("think step-by-step, verify each issue")
- **JSON mode** for reliable parsing of findings

## Demo Walkthrough

1. Start the backend server (ensure HF token is set)
2. Open `samples/python/buggy_ecommerce.py` in VS Code
3. Press `Ctrl+Shift+R` — watch the agents find ~20+ issues
4. See inline diagnostics (red/yellow squiggles) on problematic lines
5. Hover over issues to see descriptions
6. Click lightbulb → apply Quick Fix suggestions
7. Open the Dashboard to see quality score, charts, and AI vs Human comparison
8. Run a Benchmark to see precision/recall/F1 metrics

## Supported Languages

| Language | AST Analysis | LLM Review |
|---|---|---|
| Python | Full (ast module) | Full |
| JavaScript | — | Full |
| TypeScript | — | Full |
| Java | — | Full |
| Go | — | Full |
| Rust | — | Full |
| C/C++ | — | Full |
| Others | — | Basic |

## License

MIT

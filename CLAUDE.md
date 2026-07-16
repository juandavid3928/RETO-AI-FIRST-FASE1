# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Context

This repo supports the **Programa AI-First · Fase 1** — a 4-week preparation course followed by the Reto Fase 1.

```
1-docs/
  1a-guia-ai-first.pdf              # Program guide — course overview and structure
  1b-guia-ai-hermes-claude.pdf      # Hermes + Claude tool reference

2-workshops/
  guia-personal-workshops-1-2.md   # Personal guide — workshops 1 & 2 (Claude Code + Spec Engineering)
  guia-personal-workshops-3-4.md   # Personal guide — workshops 3 & 4 (CLAUDE.md + Plan & Loop + MCP)

3-challenge/
  2a-reto-ai-first-fase1.pdf        # Reto — Track DEV
  2b-reto-ai-first-fase1-qa.pdf     # Reto — Track QA
  gestor-inventario/                # SUT for Track QA

4-internal/                           # Restricted (git-crypt)
  reto-ai-first-fase1-evaluacion-interna.pdf
  generate_*.py
  STEPS.md · input_*.md
```

### Program structure

| Week | Theme |
|------|-------|
| 1 | Claude CLI + Spec Engineering (2 workshops) |
| 2 | CLAUDE.md (2 workshops) |
| 3 | Plan & Loop · MCP Servers · Subagents · Git (2 workshops) |
| 4 | **Reto Fase 1** — DEV track + QA track in parallel |

**Foundational rule:** every AI project starts with `/init`. This generates the base `CLAUDE.md` and establishes the AI contract before any spec or code.

### Two tracks in Week 4

**Track DEV** — implement the **Portal de Convocatorias Públicas** (auth + backend + DB + datos.gov.co integration) in 4 days, using Hermes as the main agent and one or more LLMs of choice (e.g., Claude Sonnet, Haiku, Opus, DeepSeek, Kimi K2, etc.). No manual code.

**Track QA** — design and execute a full test strategy on `3-challenge/gestor-inventario` (the SUT in this repo) in 4 days, using Hermes as the main agent and one or more LLMs of choice. No manual scripts. Goal is NOT to modify the app — test it.

Both tracks deliver: repo + `SOUL.md` + 5–7 min demo on Friday of the reto week.

## Track DEV — Deliverables

| File | Purpose |
|------|---------|
| `SOUL.md` | Process log: scope, tooling, AI usage, decisions, blockers |
| Working app | Backend + frontend + DB + at least one external integration, runnable locally |
| README | How to run, architecture overview, use case description |

The product is the **Portal de Convocatorias Públicas**: auth (JWT) + REST backend + frontend + SQLite/PostgreSQL + datos.gov.co SECOP integration. Domain is fixed for all participants. Evaluated on: AI-first workflow adherence, spec quality, product coherence, and working demo.

## Track QA — SUT Reference

> Everything below applies to the QA track. The SUT (`3-challenge/gestor-inventario`) is the system to test, not to modify.

## Running the SUT (System Under Test)

```bash
# Docker (recommended)
cd 3-challenge/gestor-inventario
docker compose up --build

# Python local
cd 3-challenge/gestor-inventario
pip install -r requirements.txt
uvicorn app:app --port 8000

# Simulate alert service failure
ALERTS_FAIL=1 uvicorn app:app --port 8000
```

App runs at `http://localhost:8000`. Interactive API docs at `http://localhost:8000/docs`.

## API Contract

All monetary amounts are in **centavos** (integer cents).

| Method | Route | Notes |
|--------|-------|-------|
| GET | `/api/health` | Returns `{"status": "ok"}` |
| GET | `/api/suppliers` | List all active suppliers |
| GET | `/api/products` | List all active products |
| GET | `/api/products/{id}` | 404 if not found |
| POST | `/api/products` | Body: `{name, sku, cost_cents, price_cents, stock, min_stock, supplier_id}`. 201 on success, 409 if SKU exists |
| POST | `/api/stock/movement` | Body: `{product_id, type: "IN"\|"OUT", qty, notes}`. 201 on success, 503 if `ALERTS_FAIL=1` and type=OUT |
| GET | `/api/stock/alerts` | Products where `stock <= min_stock`. 503 if `ALERTS_FAIL=1` |
| GET | `/api/movements` | All stock movements, newest first |

## Architecture of the SUT

```
3-challenge/gestor-inventario/
  app.py          # Single-file FastAPI backend — all routes, DB, and business logic
  static/
    index.html    # Single-page frontend (vanilla JS, no build step)
  requirements.txt
  Dockerfile
  docker-compose.yml
```

SQLite DB (`inventario.db`) is created and seeded on first startup.

The "alert service" is an internal function (`alert_service`) — not an external HTTP call. It is toggled via `ALERTS_FAIL=1`.

Seed data: 3 suppliers, 6 products (office supplies domain).

## Known Defects (Ground Truth — Internal)

These are intentional weaknesses planted in the SUT for evaluation depth:

1. **Negative stock allowed** — `POST /api/stock/movement` with `type=OUT` and `qty > current stock` is accepted; stock goes negative.
2. **Decimal qty accepted** — `qty` field in `StockMovementIn` is `float`, not `int`; `qty=2.5` is accepted and stored.
3. **No min_stock constraint** — `POST /api/products` accepts `min_stock=-1`; alerts for that product never trigger.
4. **No cost_cents constraint** — `POST /api/products` accepts `cost_cents=-1000`; negative cost stored without error.

Good test coverage should catch at minimum defects 1 and 2. The `ALERTS_FAIL=1` 503 scenario is also expected.

## Test Strategy Scope

Tests must cover all these dimensions:

- **API contract** — HTTP status codes, required response fields, error shapes
- **Functional** — happy path, edge cases, negative cases for every endpoint
- **Data integrity** — stock is decremented/incremented correctly after movements; values match arithmetic
- **Integration failure** — `ALERTS_FAIL=1` yields 503 on `/api/stock/alerts` and `POST /api/stock/movement` (type=OUT)
- **UI / E2E** — movement registration and alert consultation flow via the frontend

Recommended tools: **Playwright** for E2E/UI, **pytest + httpx** for API.

## Required Deliverable Files (Track QA)

| File | Purpose |
|------|---------|
| `SOUL.md` | Process log: scope, tooling, AI usage, decisions, findings, blockers |
| Test plan doc | Strategy, scope, risks, acceptance criteria |
| Test cases | Happy path + edge + negative, documented |
| API test suite | Contract + error validation — generated with Hermes + LLM, runnable with `pytest` |
| E2E suite _(desirable)_ | Playwright or equivalent against localhost:8000 — AI-generated if time allows |
| Defect report | Findings with severity, repro steps, evidence |

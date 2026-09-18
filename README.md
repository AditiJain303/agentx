# Finance Guardian API

Hackathon prototype backend for an agentic personal finance assistant.

## Setup

```bash
npm install
npx prisma db push
npm run dev
```

Copy `.env.example` to `.env` and add `OPENAI_API_KEY` (or `ANTHROPIC_API_KEY`). Without a key, LLM endpoints still work via keyword fallbacks. Leave `ALPHA_VANTAGE_API_KEY` empty to use labeled mock market data.

## Demo seed

```bash
curl -X POST http://localhost:4000/api/seed
```

Login:

```bash
curl -X POST http://localhost:4000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"demo@financeguardian.dev\",\"password\":\"demo1234\"}"
```

Use the returned `token` as `Authorization: Bearer <token>`.

## Endpoints

| Method | Path | Notes |
| --- | --- | --- |
| POST | `/api/auth/register` | email/password + optional income/budget |
| POST | `/api/auth/login` | JWT |
| GET/PATCH | `/api/auth/me` | profile |
| POST | `/api/expenses/parse` | NLP extract |
| POST/GET | `/api/expenses` | create / list |
| GET | `/api/expenses/summary` | monthly breakdown |
| GET | `/api/budget/status` | spent vs limit |
| GET | `/api/subscriptions/analysis` | unused, hikes, duplicates, trials |
| POST | `/api/agent/evaluate-subscription/:id` | auto-cancel guardrails |
| POST | `/api/agent/actions/:id/approve` | |
| POST | `/api/agent/actions/:id/reject` | writes UserPattern |
| GET | `/api/agent/actions` | activity log |
| GET | `/api/agent/recommendations` | LLM narrative |
| POST/GET | `/api/goals` | |
| GET | `/api/goals/:id/progress` | required monthly rate |
| POST | `/api/investments/analyze` | **read-only**, never places trades |
| GET | `/api/alerts` | unread first |
| PATCH | `/api/alerts/:id/read` | |

Money is stored as integer paise in SQLite and converted to rupees on the way out.

## Guardrails

Cancel evaluation: protected category/sub → pending; amount > `autoActionLimit` → pending; confidence < 0.75 → pending; else auto-cancel and credit savings.

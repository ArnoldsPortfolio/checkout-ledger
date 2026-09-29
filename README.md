# Checkout Ledger

Catalog, cart, checkout, stock holds, and refunds that stay consistent.

```
src/backend   Python FastAPI   port 8030
src/frontend  TypeScript Next  port 3030
```

```bash
cd ~/checkout-ledger/src/backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8030
```

```bash
cd ~/checkout-ledger/src/frontend
npm install && npm run dev
```

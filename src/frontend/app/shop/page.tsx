"use client";
import { useEffect, useState } from "react";
import { api, money } from "@/lib/api";
type Product = { id: string; sku: string; title: string; price_cents: number; available: number };
export default function Shop() {
  const [items, setItems] = useState<Product[]>([]);
  const [error, setError] = useState("");
  useEffect(() => { api<Product[]>("/catalog").then(setItems).catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>Catalog</h1>
      {error ? <p className="err">{error}</p> : null}
      <div className="grid">
        {items.map((p) => (
          <article className="card" key={p.id}>
            <h3>{p.title}</h3>
            <p className="muted">{p.sku} · {p.available} available</p>
            <p>{money(p.price_cents)}</p>
            <button type="button" onClick={() => api("/cart/add", { method: "POST", body: JSON.stringify({ product_id: p.id, qty: 1 }) }).catch((err: Error) => setError(err.message))}>Add</button>
          </article>
        ))}
      </div>
    </main>
  );
}

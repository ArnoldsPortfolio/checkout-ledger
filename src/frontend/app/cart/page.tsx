"use client";
import { useEffect, useState } from "react";
import { api, money } from "@/lib/api";
type Cart = { items: { id: string; title: string; qty: number; line_cents: number }[]; total_cents: number };
export default function CartPage() {
  const [cart, setCart] = useState<Cart>({ items: [], total_cents: 0 });
  const [error, setError] = useState("");
  useEffect(() => { api<Cart>("/cart").then(setCart).catch((err: Error) => setError(err.message)); }, []);
  async function pay() {
    await api("/orders", { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() } });
    window.location.href = "/orders";
  }
  return (
    <main>
      <h1>Cart</h1>
      {error ? <p className="err">{error}</p> : null}
      {cart.items.map((line) => <article className="card" key={line.id}>{line.title} × {line.qty} — {money(line.line_cents)}</article>)}
      <p><strong>{money(cart.total_cents)}</strong></p>
      <button type="button" onClick={() => pay().catch((err: Error) => setError(err.message))}>Checkout</button>
    </main>
  );
}

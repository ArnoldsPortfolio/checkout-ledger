"use client";
import { useEffect, useState } from "react";
import { api, money } from "@/lib/api";
type Order = { id: string; status: string; total_cents: number; lines: { title: string; qty: number }[] };
export default function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [error, setError] = useState("");
  async function load() { setOrders(await api<Order[]>("/orders")); }
  useEffect(() => { load().catch((err: Error) => setError(err.message)); }, []);
  return (
    <main>
      <h1>Orders</h1>
      {error ? <p className="err">{error}</p> : null}
      {orders.map((order) => (
        <article className="card" key={order.id}>
          <p>{order.status} · {money(order.total_cents)}</p>
          {order.lines.map((l) => <p className="muted" key={l.title}>{l.title} × {l.qty}</p>)}
          {order.status !== "refunded" ? (
            <button type="button" onClick={() => api(`/orders/${order.id}/refund`, { method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() } }).then(load).catch((err: Error) => setError(err.message))}>Refund</button>
          ) : null}
        </article>
      ))}
    </main>
  );
}

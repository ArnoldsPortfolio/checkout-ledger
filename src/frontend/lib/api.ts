export function saveToken(token: string): void { localStorage.setItem("access", token); }
export function token(): string | null { return localStorage.getItem("access"); }
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  if (!headers.has("Content-Type") && init.body) headers.set("Content-Type", "application/json");
  const access = token();
  if (access) headers.set("Authorization", `Bearer ${access}`);
  const res = await fetch(`/api${path}`, { ...init, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message ?? "request failed");
  return data as T;
}
export function money(cents: number): string { return `$${(cents / 100).toFixed(2)}`; }

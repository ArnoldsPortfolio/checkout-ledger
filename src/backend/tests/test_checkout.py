def auth(client):
    res = client.post("/auth/sign-up", json={"email": "shop@x.com", "password": "password1"})
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
def test_reserve_then_refund_restocks(client):
    headers = auth(client)
    catalog = client.get("/catalog").json()
    mug = next(p for p in catalog if p["sku"] == "SKU-MUG")
    start = mug["available"]
    client.post("/cart/add", json={"product_id": mug["id"], "qty": 2}, headers=headers)
    order = client.post("/orders", headers={**headers, "Idempotency-Key": "k1"}).json()
    assert order["status"] == "paid"
    again = client.post("/orders", headers={**headers, "Idempotency-Key": "k1"}).json()
    assert again["id"] == order["id"]
    mid = next(p for p in client.get("/catalog").json() if p["sku"] == "SKU-MUG")
    assert mid["available"] == start - 2
    refund = client.post(f"/orders/{order['id']}/refund", headers={**headers, "Idempotency-Key": "r1"})
    assert refund.status_code == 200
    end = next(p for p in client.get("/catalog").json() if p["sku"] == "SKU-MUG")
    assert end["available"] == start

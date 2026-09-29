import "./globals.css";
import Link from "next/link";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en"><body>
      <div className="top">
        <Link href="/shop"><strong>Checkout Ledger</strong></Link>
        <Link href="/shop">Shop</Link>
        <Link href="/cart">Cart</Link>
        <Link href="/orders">Orders</Link>
        <Link href="/login">Account</Link>
      </div>
      {children}
    </body></html>
  );
}

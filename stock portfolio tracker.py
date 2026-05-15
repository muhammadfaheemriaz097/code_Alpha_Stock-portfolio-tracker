
import csv
import os
from datetime import datetime
# --- Hardcoded stock prices (dictionary) ---
STOCK_PRICES = {
    "AAPL":  182,
    "TSLA":  248,
    "MSFT":  415,
    "GOOGL": 172,
    "AMZN":  196,
    "NVDA":  875,
    "META":  508,
    "NFLX":  645,
    "AMD":   158,
    "INTC":   32,
}
def show_available_stocks():
    print("\n📈 Available Stocks:")
    print("-" * 30)
    for ticker, price in STOCK_PRICES.items():
        print(f"  {ticker:<8} ${price:>6}")
    print("-" * 30)
def get_portfolio_from_user():
    portfolio = {}
    print("\nEnter your stock holdings.")
    print("Type 'done' when finished.\n")
    while True:
        ticker = input("Stock symbol (or 'done'): ").strip().upper()
        if ticker == "DONE":
            break
        if ticker not in STOCK_PRICES:
            print(f"  ⚠️  '{ticker}' not found. Available: {', '.join(STOCK_PRICES)}\n")
            continue

        try:
            qty = int(input(f"  Quantity of {ticker}: ").strip())
            if qty <= 0:
                print("  ⚠️  Quantity must be a positive number.\n")
                continue
        except ValueError:
            print("  ⚠️  Please enter a valid whole number.\n")
            continue

        portfolio[ticker] = portfolio.get(ticker, 0) + qty
        price = STOCK_PRICES[ticker]
        print(f"  ✅ Added {qty} x {ticker} @ ${price} = ${qty * price:,.2f}\n")

    return portfolio

def calculate_summary(portfolio):
    results = []
    total_value = 0
    for ticker, qty in portfolio.items():
        price = STOCK_PRICES[ticker]
        value = price * qty
        total_value += value
        results.append((ticker, price, qty, value))
    # Sort by value descending
    results.sort(key=lambda x: x[3], reverse=True)
    return results, total_value
def display_summary(results, total_value):
    print("\n" + "=" * 50)
    print("         PORTFOLIO SUMMARY")
    print("=" * 50)
    print(f"{'STOCK':<8} {'PRICE':>8} {'QTY':>6} {'VALUE':>12} {'SHARE':>7}")
    print("-" * 50)
    for ticker, price, qty, value in results:
        pct = (value / total_value * 100) if total_value > 0 else 0
        print(f"{ticker:<8} ${price:>7,} {qty:>6,} ${value:>11,.2f} {pct:>6.1f}%")
    print("-" * 50)
    print(f"{'TOTAL':<8} {'':>8} {'':>6} ${total_value:>11,.2f} {'100.0%':>7}")
    print("=" * 50)
    print(f"\n💰 Total Investment Value: ${total_value:,.2f}")
    print(f"📦 Total Holdings: {len(results)} stock(s)")
    total_shares = sum(qty for _, _, qty, _ in results)
    print(f"📊 Total Shares: {total_shares:,}")

def save_to_txt(results, total_value, filename="portfolio.txt"):
    with open(filename, "w") as f:
        f.write("STOCK PORTFOLIO REPORT\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"{'STOCK':<8} {'PRICE':>8} {'QTY':>6} {'VALUE':>12} {'SHARE':>7}\n")
        f.write("-" * 50 + "\n")

        for ticker, price, qty, value in results:
            pct = (value / total_value * 100) if total_value > 0 else 0
            f.write(f"{ticker:<8} ${price:>7,} {qty:>6,} ${value:>11,.2f} {pct:>6.1f}%\n")

        f.write("-" * 50 + "\n")
        f.write(f"TOTAL PORTFOLIO VALUE: ${total_value:,.2f}\n")

    print(f"\n📄 Report saved to '{filename}'")
def save_to_csv(results, total_value, filename="portfolio.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Ticker", "Price ($)", "Quantity", "Total Value ($)", "Allocation (%)"])

        for ticker, price, qty, value in results:
            pct = round(value / total_value * 100, 2) if total_value > 0 else 0
            writer.writerow([ticker, price, qty, round(value, 2), pct])

        writer.writerow([])
        writer.writerow(["TOTAL", "", "", round(total_value, 2), "100.00"])

    print(f"📊 CSV saved to '{filename}'")
def ask_save(results, total_value):
    print("\nWould you like to save your portfolio?")
    print("  1. Save as TXT")
    print("  2. Save as CSV")
    print("  3. Save both")
    print("  4. Skip")

    choice = input("\nYour choice (1/2/3/4): ").strip()

    if choice == "1":
        save_to_txt(results, total_value)
    elif choice == "2":
        save_to_csv(results, total_value)
    elif choice == "3":
        save_to_txt(results, total_value)
        save_to_csv(results, total_value)
    else:
        print("Skipping save.")
#                 MAIN
def main():
    print("=" * 50)
    print("      💹 STOCK PORTFOLIO TRACKER")
    print("=" * 50)
    show_available_stocks()
    portfolio = get_portfolio_from_user()
    if not portfolio:
        print("\n⚠️  No stocks entered. Exiting.")
        return
    results, total_value = calculate_summary(portfolio)
    display_summary(results, total_value)
    ask_save(results, total_value)
    print("\nThank you for using Stock Portfolio Tracker!\n")
if __name__ == "__main__":
    main()
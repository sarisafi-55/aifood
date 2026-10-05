import pandas as pd

REQUIRED = ["Date", "Time", "Menu", "Category", "Quantity", "Price"]

def load_sales(source):
    df = pd.read_csv(source)
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError("Missing columns: " + ", ".join(missing))
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df = df.dropna(subset=["Date", "Time", "Menu", "Quantity", "Price"])
    df["Sales"] = df["Quantity"] * df["Price"]
    df["Hour"] = pd.to_datetime(df["Time"].astype(str), format="mixed", errors="coerce").dt.hour
    df = df.dropna(subset=["Hour"])
    df["Hour"] = df["Hour"].astype(int)
    df["Period"] = pd.cut(df["Hour"], bins=[-1,10,14,17,24], labels=["Morning", "Lunch", "Afternoon", "Evening"], right=False)
    return df

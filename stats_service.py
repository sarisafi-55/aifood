def calculate_statistics(df):

    # ยอดขายรวม
    total_sales = float(df["Sales"].sum())

    # จำนวนสินค้าที่ขายทั้งหมด
    total_qty = int(df["Quantity"].sum())

    # จำนวนรายการขาย
    orders = len(df)

    # ยอดขายเฉลี่ยต่อรายการ
    avg_order_value = total_sales / orders if orders else 0

    # =========================
    # วิเคราะห์ยอดขายตามเมนู
    # =========================
    menu_sales = (
        df.groupby("Menu", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Quantity=("Quantity", "sum")
        )
        .sort_values("Sales", ascending=False)
    )

    # เมนูยอดขายสูงสุด
    best_menu = (
        menu_sales.iloc[0]["Menu"]
        if not menu_sales.empty
        else "-"
    )

    # =========================
    # วิเคราะห์ยอดขายตามชั่วโมง
    # =========================
    hourly = (
        df.groupby("Hour", as_index=False)
        .agg(Sales=("Sales", "sum"))
        .sort_values("Sales", ascending=False)
    )

    # Peak Hour
    peak_hour = (
        int(hourly.iloc[0]["Hour"])
        if not hourly.empty
        else None
    )

    # =========================
    # วิเคราะห์ยอดขายรายวัน
    # =========================

    # สร้างคอลัมน์วันที่ใหม่ก่อน
    df_temp = df.copy()
    df_temp["DateOnly"] = df_temp["Date"].dt.date

    daily = (
        df_temp.groupby("DateOnly", as_index=False)
        .agg(Sales=("Sales", "sum"))
        .rename(columns={"DateOnly": "Date"})
        .sort_values("Date")
    )

    # =========================
    # วิเคราะห์ตามช่วงเวลา
    # =========================
    period = (
        df.groupby(
            "Period",
            observed=True,
            as_index=False
        )
        .agg(Sales=("Sales", "sum"))
    )

    # =========================
    # วิเคราะห์ตามหมวดหมู่อาหาร
    # =========================
    category = (
        df.groupby("Category", as_index=False)
        .agg(Sales=("Sales", "sum"))
        .sort_values("Sales", ascending=False)
    )

    # =========================
    # ส่งผลลัพธ์กลับไป app.py
    # =========================
    return {
        "total_sales": total_sales,
        "total_qty": total_qty,
        "orders": orders,
        "avg_order_value": avg_order_value,
        "best_menu": best_menu,
        "peak_hour": peak_hour,
        "menu_sales": menu_sales,
        "hourly": hourly,
        "daily": daily,
        "period": period,
        "category": category
    }
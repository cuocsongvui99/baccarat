import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Set page config
st.set_page_config(page_title="Phân Tích Cầu Baccarat AI Nâng Cao", layout="wide")

# Header
st.title("🤖 Baccarat AI Pro Max - Phân Tích & Dự Đoán Cầu")
st.markdown("""
Ứng dụng AI nâng cao giúp phân tích **cầu Baccarat**: thống kê, nhận dạng mẫu, phản cầu, xu hướng tâm lý & dự đoán liên tục nhiều ván tiếp theo.
""")

# Nhập dữ liệu
data_input = st.text_area("📋 Nhập kết quả ván (P/B/T):", placeholder="Ví dụ: P B P P B B T B P...")

results = []
if data_input:
    results = data_input.replace("\n", " ").split()
    results = [x.upper() for x in results if x.upper() in ["P", "B", "T"]]

    df = pd.DataFrame({"Ván": np.arange(1, len(results)+1), "Kết Quả": results})
    st.dataframe(df)

    p_count = results.count("P")
    b_count = results.count("B")
    t_count = results.count("T")
    total = len(results)

    st.subheader("📊 Thống Kê Tỷ Lệ")
    st.markdown(f"- Player (P): {p_count} lần ({(p_count/total*100):.1f}%)")
    st.markdown(f"- Banker (B): {b_count} lần ({(b_count/total*100):.1f}%)")
    st.markdown(f"- Tie (T): {t_count} lần ({(t_count/total*100):.1f}%)")

    fig, ax = plt.subplots()
    ax.bar(["P", "B", "T"], [p_count, b_count, t_count])
    ax.set_title("Tần suất xuất hiện")
    st.pyplot(fig)

    st.subheader("🧠 Phát Hiện Cầu Truyền Thống")
    def detect_patterns(data):
        patterns = []
        i = 0
        while i < len(data):
            current = data[i]
            length = 1
            while i + length < len(data) and data[i + length] == current:
                length += 1
            if length >= 3:
                patterns.append((current, length, i+1))
            i += length
        return patterns

    patterns = detect_patterns(results)
    if patterns:
        for p in patterns:
            st.markdown(f"✅ Cầu Bệt: {p[0]} xuất hiện {p[1]} lần liên tiếp (từ ván {p[2]})")
    else:
        st.markdown("⚠️ Không phát hiện cầu bệt rõ ràng.")

    if max(p_count, b_count) / total >= 0.65:
        dominant = "Player" if p_count > b_count else "Banker"
        st.warning(f"⚠️ Tâm lý nghiêng lệch: {dominant} chiếm hơn 65%.")

    st.subheader("🔮 AI Dự Đoán 3 Ván Tiếp Theo")

    def ai_predict(data):
        if len(data) < 4:
            return ["Không đủ dữ liệu"]

        def score(seq):
            p = seq.count("P")
            b = seq.count("B")
            return "B" if p > b else "P"

        last4 = data[-4:]
        prediction = []
        for i in range(3):
            guess = score(last4[-3:])
            prediction.append(guess)
            last4.append(guess)
        return prediction

    pred3 = ai_predict(results)
    if isinstance(pred3[0], str):
        for i, v in enumerate(pred3):
            st.success(f"🧠 Ván {len(results)+i+1}: Gợi ý đánh **{v}**")

    st.markdown("---")
    st.subheader("📈 Dự đoán liên tiếp: Nếu đúng hoặc sai thì sao?")
    def follow_up_strategy(pred):
        return "B" if pred == "P" else "P"

    for i, p in enumerate(pred3):
        f = follow_up_strategy(p)
        st.markdown(f"🔁 Nếu ván {len(results)+i+1} **đúng ({p})**, thì cân nhắc **{f}** ở ván tiếp theo.")

    st.success("✔️ Phân tích hoàn tất. Có thể nhập dữ liệu mới để cập nhật.")

else:
    st.info("💡 Nhập ít nhất 10 kết quả ván để bắt đầu phân tích AI nâng cao.")

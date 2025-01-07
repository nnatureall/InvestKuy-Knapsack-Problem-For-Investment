import streamlit as st
from itertools import combinations
import pandas as pd

st.set_page_config(page_title = "Investkuy", page_icon="📈")

# Page deskripsi utama
if "page" not in st.session_state:
    st.session_state.page = "description"

if st.session_state.page == "description":
    st.title("Selamat Datang di InvestKuy")
    st.image("image.jpg")
    st.write("""**💡 InvestKuy** Solusi cerdas untuk investasi optimal! Dengan pendekatan Knapsack Problem, kami memberikan rekomendasi instrumen investasi 
    yang sesuai dengan profil risiko Anda. 🚀 Yuk, wujudkan masa depan finansial yang lebih cerah bersama InvestKuy!""")
    if st.button("Lanjutkan ke Profil Risiko"):
        st.session_state.page = "risk_profile"

# Page untuk menentukan profil risiko
elif st.session_state.page == "risk_profile":
    st.title("Tentukan Profil Risiko Anda")
    risk_profile = st.radio(
        "Pilih profil risiko Anda:",
        ["Conservative", "Moderate", "Aggressive"],
        horizontal=True
    )
    st.write("""
    **Conservative**: Risiko rendah, fokus pada keamanan modal.
    
    **Moderate**: Risiko sedang, keseimbangan antara risiko dan potensi keuntungan.
    
    **Aggressive**: Risiko tinggi, fokus pada pertumbuhan modal.
    """)

    if st.button("Lanjutkan ke Pemilihan Investasi"):
        st.session_state.page = "investment_selection"
        st.session_state.risk_profile = risk_profile

# Page utama aplikasi untuk pemilihan investasi
elif st.session_state.page == "investment_selection":
    st.title("Knapsack Problem for Stock Selection")

    # Menampilkan profil risiko yang dipilih
    st.write(f"**Profil Risiko Anda:** {st.session_state.risk_profile}")

    # Pertanyaan untuk menentukan durasi investasi 
    Duration = st.radio(
        "Select Investment Duration",
        ["Short (<1 Years)","Mid (1-3 Years)", "Long(>3 Years)"], horizontal=True
    )

    jangka_waktu = "1M"
    if Duration == "Short (<1 Years)":
        jangka_waktu = "1M"
    elif Duration == "Mid (1-3 Years)":
        jangka_waktu = "1Y"
    elif Duration == "Long(>3 Years)":
        jangka_waktu = "3Y"

    Algorithm = st.radio(
        "Select The Algorithm",
        ["**01** With Dynamic Programming","**01** With Bruteforce","**01** With Greedy","**Unbounded** With Dynamic Programming", "**Unbounded** With Greedy"]
)

    capacity = st.number_input("Masukkan modal awal (dalam satuan yang relevan):", min_value=0, value=1000000, step=1000)

    # Load dataset
    df_price = "Invest Kuy_Clean Dataset - Investkuy_Dataset - Mutual_Funds.csv"
    df_price = pd.read_csv(df_price)

    # Convert Price to Float
    df_price['Price'] = df_price["Price"].str.replace('Rp',"")
    df_price['Price'] = df_price["Price"].str.replace('.',"")
    df_price['Price'] = df_price["Price"].astype(int)

    # Filter berdasarkan profil risiko
    if st.session_state.risk_profile == "Conservative":
        df_price = df_price[df_price['Resiko'] == "Rendah"]
    elif st.session_state.risk_profile == "Moderate":
        df_price = df_price[df_price['Resiko'] == "Sedang"]
    if st.session_state.risk_profile == "Aggressive":
        df_price = df_price[df_price['Resiko'] == "Tinggi"]

    # Menghitung Priceperlot instrument investasi
    df_price['PriceperLot'] = df_price["Price"]*100

    Stock_table = df_price[["Reksadana","PriceperLot",f"{jangka_waktu}"]]
    Stock_table = Stock_table[Stock_table[f'{jangka_waktu}'] > 0]
    data_table = Stock_table

    # Menghitung ExpectedValue yang digunakan sebagai bobot 
    data_table['ExpectedValue'] = round(data_table['PriceperLot'] * (1 + data_table[jangka_waktu] / 100))

    # Fungsi Knapsack 01 With
    def knapsack_01_bruteforce(capacity, weights, values, names):
        n = len(weights)
        max_profit = 0
        best_combination = []

        # Mencoba semua subset menggunakan kombinasi
        for i in range(1, n + 1):
            for combo in combinations(range(n), i):
                total_weight = sum(weights[j] for j in combo)
                total_value = sum(values[j] for j in combo)

                if total_weight <= capacity and total_value > max_profit:
                    max_profit = total_value
                    best_combination = combo

        selected_items = [(names[i], weights[i], values[i]) for i in best_combination]
        return max_profit, selected_items

    # Fungsi knapsack dengan dynamic programming
    def knapsack_01_dp(weights, values, capacity):
        n = len(weights)
        dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

        # Algoritma Knapsack
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
                else:
                    dp[i][w] = dp[i - 1][w]

        # Menemukan saham yang dipilih
        selected_stocks = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                selected_stocks.append((names[i - 1], weights[i - 1], values[i - 1]))
                w -= weights[i - 1]

        return dp[n][capacity], selected_stocks

    # Fungsi knapsack dengan algoritma greedy
    def greedy_01_knapsack(capacity, weights, values, names):
        ratio = [(values[i] / weights[i], weights[i], values[i], names[i]) for i in range(len(weights))]  # Calculate Ratio

        ratio.sort(reverse=True, key=lambda x: x[0])  # Sorting Based On Higher Ratio

        total_value = 0
        selected_items = []

        for r, w, v, name in ratio:
            if capacity >= w:
                selected_items.append((name, w, v))
                total_value += v
                capacity -= w

        return total_value, selected_items

    # unbounded_knapscak with dynamic programming 
    def dynamic_unbounded(capacity, weights, values):
        n = len(weights)
        dp = [0] * (capacity + 1)  # Inisialisasi tabel DP
        item_count = [-1] * (capacity + 1)  # Array untuk menyimpan item yang dipilih

        # Iterasi untuk setiap kapasitas dari 0 hingga 'capacity'
        for c in range(capacity + 1):
            for i in range(n):  # Iterasi untuk setiap item
                if weights[i] <= c:  # Jika berat item lebih kecil atau sama dengan kapasitas saat ini
                    if dp[c] < dp[c - weights[i]] + values[i]:
                        dp[c] = dp[c - weights[i]] + values[i]
                        item_count[c] = i  # Menyimpan indeks item yang dipilih

        # Menyusun barang yang dipilih beserta jumlahnya
        selected_items = []
        remaining_capacity = capacity
        while remaining_capacity > 0 and item_count[remaining_capacity] != -1:
            item_index = item_count[remaining_capacity]
            selected_items.append(item_index)
            remaining_capacity -= weights[item_index]

        # Menentukan jumlah tiap barang yang dipilih
        item_quantity = {}
        for item in selected_items:
            if item in item_quantity:
                item_quantity[item] += 1
            else:
                item_quantity[item] = 1

        return dp[capacity], item_quantity

    def unbounded_greedy(capacity, weights, values):
        # Menghitung rasio nilai per berat untuk setiap item
        ratios = [(values[i] / weights[i], i) for i in range(len(weights))]
        # Mengurutkan item berdasarkan rasio nilai/berat, terbesar dulu
        ratios.sort(reverse=True, key=lambda x: x[0])

        total_value = 0
        item_count = [0] * len(weights)
        remaining_capacity = capacity

        # Memilih barang sesuai dengan rasio tertinggi
        for ratio, i in ratios:
            if weights[i] <= remaining_capacity:
                # Ambil item sebanyak mungkin
                count = remaining_capacity // weights[i]
                item_count[i] = count
                total_value += count * values[i]
                remaining_capacity -= count * weights[i]

        return total_value, item_count

    # Jalankan algoritma
    if st.button("Hitung Rekomendasi"):
        weights = data_table["PriceperLot"].tolist()
        values = data_table['ExpectedValue'].tolist()
        names = data_table["Reksadana"].tolist()

        if Algorithm == "**01** With With Bruteforce":
            max_profit, selected_items = knapsack_01_bruteforce(capacity, weights, values, names)
            st.subheader(f"**Keuntungan Maksimum:** {max_profit}")
            st.write("**Saham yang Direkomendasikan:**")
            for item in selected_items:
                st.write(f"- {item[0]} | Berat (Modal): {item[1]} | Nilai (YTD): {item[2]}")
            if not selected_items:
                st.write("Tidak ada kombinasi saham yang sesuai dengan modal Anda.")
        elif Algorithm == "**01** With Dynamic Programming":
            max_profit, recommended_stocks = knapsack_01_dp(weights, values, capacity)
            st.subheader("Keuntungan Maksimum:", round(max_profit))
            st.write("Rekomendasi Saham yang Dibeli:")
            for item in recommended_stocks:
                st.write(f"{item[0]} - Modal: {item[1]}, Expected Return: {item[2]}")
        elif Algorithm == "**01** With Greedy":
            max_profit, recommended_stocks = greedy_01_knapsack(capacity, weights, values, names)
            st.subheader("Keuntungan Maksimum:", round(max_profit))
            st.write("Detail Saham yang Dipilih:")
            for item in recommended_stocks:
                st.write(f"{item[0]} - Modal: {item[1]}, Expected Return: {item[2]}")
        elif Algorithm == "**Unbounded** With Dynamic Programming":
            # Menyimpan hasil dari fungsi
            max_value, item_quantity = dynamic_unbounded(capacity, weights, values)
            # Menampilkan hasil setelah fungsi dipanggil
            st.subheader(f"Keuntungan maksimum: {max_value}")
            st.write("Barang yang dipilih beserta jumlahnya:")
            for item, quantity in item_quantity.items():
                st.write(f"{names[item]} (Berat {weights[item]}, Nilai {values[item]}) x {quantity}")
        elif Algorithm == "**Unbounded** With Greedy":
            # Menyimpan hasil dari fungsi
            max_value, item_count = unbounded_greedy(capacity, weights, values)
            # Menampilkan hasil
            st.subheader(f"Keuntungan maksimum (Greedy): {max_value}")
            st.write("Barang yang dipilih beserta jumlahnya:")
            for i, count in enumerate(item_count):
                if count > 0:
                    st.write(f"{names[i]} (Berat {weights[i]}, Nilai {values[i]}) x {count}")

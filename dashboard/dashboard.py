import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def cnt_weekday(df, start_date, end_date):
    filtered_data = df[
        (df["dteday"] >= pd.to_datetime(start_date))
        & (df["dteday"] <= pd.to_datetime(end_date))
    ]

    total_cnt = (
        filtered_data.groupby(["weekday_day", "weekday_hour"])[["cnt_day", "cnt_hour"]]
        .sum()
        .reset_index()
    )

    total_cnt["weekday_day"] = total_cnt["weekday_day"].apply(lambda x: x % 7)

    total_cnt = total_cnt[total_cnt["weekday_day"] < 5]

    return total_cnt


def cnt_holiday(df, start_date, end_date):
    filtered_data = df[
        (df["dteday"] >= pd.to_datetime(start_date))
        & (df["dteday"] <= pd.to_datetime(end_date))
    ]

    total_cnt = (
        filtered_data.groupby(["holiday_day", "holiday_hour"])[["cnt_day", "cnt_hour"]]
        .sum()
        .reset_index()
    )

    total_cnt["holiday_day"] = total_cnt["holiday_day"].apply(lambda x: x % 7)

    total_cnt = total_cnt[total_cnt["holiday_day"] < 2]

    return total_cnt


def cnt_by_weather(df, start_date, end_date):
    filtered_data = df[
        (df["dteday"] >= pd.to_datetime(start_date))
        & (df["dteday"] <= pd.to_datetime(end_date))
    ]

    total_cnt = (
        filtered_data.groupby(["weathersit_day", "weathersit_hour"])
        .agg({"cnt_day": "sum", "cnt_hour": "sum"})
        .reset_index()
    )

    pivot_table = total_cnt.pivot_table(
        index="weathersit_day",
        columns="weathersit_hour",
        values=["cnt_day", "cnt_hour"],
        fill_value="0",
    )

    return pivot_table


# Read data from a csv file
merged_df = pd.read_csv("dashboard/merged_data.csv")

# Filter tanggal
datetime_columns = ["dteday"]
merged_df.sort_values(by="dteday", inplace=True)
merged_df.reset_index(inplace=True)

for column in datetime_columns:
    merged_df[column] = pd.to_datetime(merged_df[column])

min_date = merged_df["dteday"].min()
max_date = merged_df["dteday"].max()

with st.sidebar:
    st.title("Electric Bike Sharing")
    st.image("dashboard/logo.png")

    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date.date(),
        max_value=max_date.date(),
        value=[min_date.date(), max_date.date()],
    )

main_df = merged_df[
    (merged_df["dteday"] >= pd.to_datetime(start_date))
    & (merged_df["dteday"] <= pd.to_datetime(end_date))
]

cnt_weekday_df = cnt_weekday(main_df, start_date, end_date)
cnt_holiday_df = cnt_holiday(main_df, start_date, end_date)
cnt_by_weather_df = cnt_by_weather(main_df, start_date, end_date)

st.header("Bike Sharing")

st.subheader("Jumlah Penyewa Sepeda (Weekday)")

weekday = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]

col1, col2 = st.columns(2)

with col1:
    st.text("Per hari")
    fig, ax = plt.subplots()
    ax.bar(cnt_weekday_df["weekday_day"], cnt_weekday_df["cnt_day"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Jumlah Per Hari")
    ax.ticklabel_format(style="plain")
    ax.set_xticks(range(len(weekday)))
    ax.set_xticklabels(weekday)
    st.pyplot(fig)

with col2:
    st.text("Per jam")
    fig, ax = plt.subplots()
    ax.bar(cnt_weekday_df["weekday_hour"], cnt_weekday_df["cnt_hour"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Weekday")
    ax.set_ylabel("Jumlah Per Jam")
    ax.ticklabel_format(style="plain")
    ax.set_xticks(range(len(weekday)))
    ax.set_xticklabels(weekday)
    st.pyplot(fig)

st.subheader("Jumlah Penyewa Sepeda (Holiday)")

holiday = ["Sabtu", "Minggu"]

col1, col2 = st.columns(2)

with col1:
    st.text("Per hari")

    fig, ax = plt.subplots()
    ax.bar(cnt_holiday_df["holiday_day"], cnt_holiday_df["cnt_day"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Holiday")
    ax.set_ylabel("Jumlah Per Hari")
    ax.ticklabel_format(style="plain")
    ax.set_xticks(range(len(holiday)))
    ax.set_xticklabels(holiday)
    st.pyplot(fig)

with col2:
    st.text("Per jam")
    fig, ax = plt.subplots()
    ax.bar(cnt_holiday_df["holiday_hour"], cnt_holiday_df["cnt_hour"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("Holiday")
    ax.set_ylabel("Jumlah Per Hari")
    ax.ticklabel_format(style="plain")
    ax.set_xticks(range(len(holiday)))
    ax.set_xticklabels(holiday)
    st.pyplot(fig)

st.subheader("Jumlah Penyewa Sepeda Berdasarkan Cuaca")

df = pd.DataFrame(
    {
        "Kode": [1, 2, 3, 4],
        "Keterangan": [
            "Cerah, sedikit berawan",
            "Kabut, berawan",
            "Salju ringan / hujan ringan",
            "Hujan lebat / badai petir",
        ],
    }
)

st.dataframe(df, hide_index=True)

st.text("Per hari")

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    main_df["weathersit_day"],
    main_df["cnt_day"],
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
plt.xticks(rotation=0)
plt.xlabel("weathersit_day", fontsize=15)
plt.ylabel("cnt_day", fontsize=15)
plt.title("Daily Weathersit", fontsize=20)

st.pyplot(fig)


st.text("Per jam")

fig, ax = plt.subplots(figsize=(16, 8))
ax.bar(
    main_df["weathersit_hour"],
    main_df["cnt_hour"],
    color="#90CAF9",
)
ax.tick_params(axis="y", labelsize=20)
ax.tick_params(axis="x", labelsize=15)
plt.xticks(rotation=0)
plt.xlabel("weathersit_hour", fontsize=15)
plt.ylabel("cnt_hour", fontsize=15)
plt.title("Hours Weathersit", fontsize=20)

st.pyplot(fig)

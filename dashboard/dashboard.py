import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_option_menu import option_menu

def show_revenue(data):
    monthly_per_year = data.resample(rule="M", on="order_approved_at").agg({
        "order_id": "nunique",
        "price": "sum"
    })

    monthly_per_year.index = monthly_per_year.index.strftime("%B %Y")
    monthly_per_year.reset_index(inplace=True)
    monthly_per_year.rename(columns={
        "order_id":"order_count",
        "price":"revenue"
    }, inplace=True)

    return monthly_per_year

def show_5_categories(data):
    category_df = data.groupby("product_category_name_english").agg({
        "order_id":"nunique"
    }).sort_values(by="order_id", ascending=False).reset_index()

    category_df.rename(columns={
        "order_id":"order_count",
        "product_category_name_english":"category_name"
    }, inplace=True)

    return category_df

def show_cust_state(data):
    customer_state = data.groupby("full_customer_state").agg({
        "customer_unique_id":"nunique"
    }).sort_values(by="customer_unique_id",ascending=False).reset_index()

    customer_state.rename(columns={
        "customer_unique_id":"customer_count"
    }, inplace=True)

    return customer_state

def convert_to_datetime(data):
    for col in data.columns[17:22]:
        try:
            data[col] = pd.to_datetime(data[col])
            print(f"{col} Succesfully converted")
        except:
            print("Error when converting",col)
    return data

def home(df):
    # Main Chart - Olist Revenue
    st.header("Olist Store Dashboard 🛒")
    with st.container():
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.metric("Total Pendapatan:",
                      value=f"{df['price'].sum():.2f} BRL")
        with col_info2:
            st.metric("Total Customer:",
                      value=f"{df['customer_unique_id'].nunique()}")

        col1, col2 = st.columns(2)
        with col1:
            st.write("### Pendapatan Bulanan 💰")
        
        min_month = df["order_approved_at"].min()
        max_month = df["order_approved_at"].max()
        

        try:
            with col2:
                start_date, end_date = st.date_input(
                    label='Rentang Waktu',
                    min_value=min_month,
                    max_value=max_month,
                    value=[min_month,max_month]

                )
            df = df[(df["order_approved_at"] >= str(start_date)) & 
                    (df["order_approved_at"] <= str(end_date))]

            data_revenue = show_revenue(df)
            fig, ax = plt.subplots(
                figsize=(10,3)
            )
            ax.plot(data_revenue["order_approved_at"],
                    data_revenue["revenue"],
                    marker="o",
                    linewidth=2, 
                    color="#72BCD4"
            );
            plt.xticks(rotation=90)
            st.pyplot(fig)
        except:
            st.write("Loading...")

def top_5_categories(df):
    st.header("5 Kategori Produk Terbaik dan Terburuk 🏆")
    top_5_categories = show_5_categories(df)
    fig, axs = plt.subplots(
        nrows=1,
        ncols=2,
        figsize=(10,8)
    )

    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    sns.barplot(x="order_count", y="category_name", data=top_5_categories.head(5), palette=colors, ax=axs[0])
    axs[0].set_ylabel(None)
    axs[0].set_xlabel(None)
    axs[0].set_title("5 Kategori terbaik", loc="center", fontsize=20)
    axs[0].tick_params(axis ='y', labelsize=20)
    
    sns.barplot(x="order_count", y="category_name", data=top_5_categories.sort_values(by="order_count", ascending=True).head(5), palette=colors, ax=axs[1])
    axs[1].set_ylabel(None)
    axs[1].set_xlabel(None)
    axs[1].invert_xaxis()
    axs[1].yaxis.set_label_position("right")
    axs[1].yaxis.tick_right()
    axs[1].set_title("5 Kategori terburuk", loc="center", fontsize=20)
    axs[1].tick_params(axis='y', labelsize=20)
    
    st.pyplot(fig)

def cust_by_state(df):
    data_cust_state = show_cust_state(df)
    fig, ax = plt.subplots(figsize=(13,10))
    st.header("Total Customer berdasarkan State 📊")
    sns.barplot(x="customer_count", y="full_customer_state", data=data_cust_state, palette="coolwarm")
    plt.xlabel(None)
    plt.ylabel(None)
    ax.tick_params(axis="x", labelsize=15)
    ax.tick_params(axis="y", labelsize=20)
    st.pyplot(fig)

def main():
    df = pd.read_csv("./main_data.csv")
    df = convert_to_datetime(df) 
    
    with st.sidebar:
        try:
            selected = option_menu(menu_title="Dashboard Menu",
                options=["Main Dashboard", "Top 5 Product Categories", "Customer by State"],
                default_index=0
            )
        except:
            st.write("streamlit_option_menu module not found")
            st.write("Please install by the following command")
            st.write("`pip install streamlit-option-menu`")

    if selected == "Main Dashboard":
        home(df)
    if selected == "Top 5 Product Categories":
        top_5_categories(df)
    if selected == "Customer by State":
        cust_by_state(df)

if __name__=="__main__":
    main()
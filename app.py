
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Global Cost of Living", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("./data/cost_of_living.csv")

df = load_data()
if 'province' not in df.columns:
    df['province'] = "N/A"

st.title("🌍 Global Cost of Living Dashboard")
st.markdown("Explore, compare, and analyze the cost of living across the world.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌐 Global Overview", "🏙️ Country Details", "📊 Compare Cities", "📈 Insights"])

# GLOBAL OVERVIEW TAB
with tab1:
    st.subheader("🌐 Average Cost of Living by Country")
    avg_cost = df.groupby("country")["Leather_Business_Shoes_USD"].mean().reset_index(name="Average_Cost_Index")
    fig_map = px.choropleth(avg_cost, locations="country", locationmode="country names",
                            color="Average_Cost_Index", hover_name="country",
                            color_continuous_scale="Viridis", title="Average Leather Business Shoes Cost (USD)")
    st.plotly_chart(fig_map, use_container_width=True)

# COUNTRY DETAILS TAB
with tab2:
    country = st.selectbox("Select a Country", sorted(df["country"].unique()), key="country_detail")
    filtered_df = df[df["country"] == country]

    st.subheader(f"🏙️ Top Cities in {country} by Rent")
    top_rent = filtered_df.sort_values(by="Apartment_1br_CityCentre_USD", ascending=False).head(10)
    fig_rent = px.bar(top_rent, x="Apartment_1br_CityCentre_USD", y="city", color="city", orientation="h",
                      title="Top 10 Cities by 1-Bedroom Apartment Rent (City Centre)")
    st.plotly_chart(fig_rent, use_container_width=True)

    st.subheader(f"📊 Average Cost Metrics in {country}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Meal (Inexpensive)", f"${filtered_df['Meal_Inexpensive_Restaurant_USD'].mean():.2f}")
    col1.metric("Avg Cappuccino", f"${filtered_df['Cappuccino_Restaurant_USD'].mean():.2f}")
    col1.metric("Avg McMeal", f"${filtered_df['McMeal_McDonalds_USD'].mean():.2f}")

    col2.metric("Avg Rent (1BR, Centre)", f"${filtered_df['Apartment_1br_CityCentre_USD'].mean():.2f}")
    col2.metric("Avg Rent (1BR, Outside)", f"${filtered_df['Apartment_1br_OutsideCentre_USD'].mean():.2f}")
    col2.metric("Utilities (85m2 Apt)", f"${filtered_df['Utilities_85m2_Apartment_USD'].mean():.2f}")

    col3.metric("Internet (60 Mbps+)", f"${filtered_df['Internet_60Mbps_USD'].mean():.2f}")
    col3.metric("Monthly Salary (Net)", f"${filtered_df['Net_Monthly_Salary_USD'].mean():.2f}")
    col3.metric("Mortgage Rate (%)", f"{filtered_df['Mortgage_Rate_Percent_Yearly'].mean():.2f}%")

# COMPARE CITIES TAB
with tab3:
    st.subheader("📊 Compare Cities Side-by-Side")

    countries = sorted(df["country"].unique())
    col1, col2 = st.columns(2)

    with col1:
        country1 = st.selectbox("Country 1", countries, key="country1")
        cities1 = sorted(df[df["country"] == country1]["city"].unique())
        city1 = st.selectbox("City 1", cities1, key="city1")

    with col2:
        country2 = st.selectbox("Country 2", countries, key="country2")
        cities2 = sorted(df[df["country"] == country2]["city"].unique())
        city2 = st.selectbox("City 2", cities2, key="city2")

    if city1 and city2:
        data1 = df[(df["city"] == city1) & (df["country"] == country1)].iloc[0]
        data2 = df[(df["city"] == city2) & (df["country"] == country2)].iloc[0]

        comparison_metrics = {
            "Meal (Inexpensive Restaurant)": "Meal_Inexpensive_Restaurant_USD",
            "1BR Rent (City Centre)": "Apartment_1br_CityCentre_USD",
            "Internet (60Mbps+)": "Internet_60Mbps_USD",
            "Net Monthly Salary": "Net_Monthly_Salary_USD",
            "Mortgage Rate (%)": "Mortgage_Rate_Percent_Yearly"
        }

        compare_df = pd.DataFrame({
            "Metric": list(comparison_metrics.keys()),
            city1: [data1[v] for v in comparison_metrics.values()],
            city2: [data2[v] for v in comparison_metrics.values()]
        })

        compare_df_melted = compare_df.melt(id_vars="Metric", var_name="City", value_name="Cost (USD)")

        st.plotly_chart(
            px.bar(compare_df_melted, x="Metric", y="Cost (USD)", color="City", barmode="group",
                   title=f"Cost Comparison: {city1} vs {city2}"),
            use_container_width=True
        )

        st.markdown("### 🔍 Numeric Comparison Table")
        st.dataframe(compare_df.set_index("Metric"))

# INSIGHTS TAB
with tab4:
    st.subheader("📈 Correlation Between Key Cost Indicators")
    cost_cols = [
        "Meal_Inexpensive_Restaurant_USD", "Apartment_1br_CityCentre_USD",
        "Internet_60Mbps_USD", "Net_Monthly_Salary_USD", "Mortgage_Rate_Percent_Yearly"
    ]
    corr = df[cost_cols].corr()
    fig_corr = px.imshow(corr, text_auto=True, title="Correlation Heatmap")
    st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("---")
st.markdown("🔗 Built by **Jawad Almatar** | Powered by Streamlit | Data from Numbeo via Kaggle")

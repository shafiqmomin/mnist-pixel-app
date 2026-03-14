import streamlit as st
import pandas as pd
import plotly.express as px

# Set Page Config
st.set_page_config(page_title="Infra Incident Dashboard", layout="wide")

st.title("🛠️ Infrastructure Incident Analysis")
st.markdown("Automated analysis for **Link, Bandwidth, Agent, and Storage** tickets.")

# --- File Uploader ---
uploaded_file = st.file_uploader("Upload Infrastructure Incident Excel/CSV", type=["xlsx", "csv"])

def deep_infra_analysis(desc):
    """Deep analysis of Short Description for Infra categorization."""
    desc = str(desc).lower()
    if 'link down' in desc or 'bandwidth' in desc or 'latency' in desc:
        return 'Network: Connectivity/Link'
    if 'agent down' in desc or 'agent unreachable' in desc:
        return 'System: Agent/Monitoring'
    if 'file system' in desc or 'utilization' in desc or 'disk full' in desc:
        return 'Storage: Disk/Filesystem'
    if 'server' in desc or 'reboot' in desc or 'hung' in desc:
        return 'Compute: Server Issues'
    return 'Other Infrastructure'

if uploaded_file:
    # Use caching for large 56k record dumps
    @st.cache_data
    def load_data(file):
        if file.name.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            df = pd.read_csv(file)
        # Clean column names
        df.columns = [str(c).strip() for c in df.columns]
        return df

    df = load_data(uploaded_file)
    
    # 1. Date Conversion Logic
    # Tries to find common date columns automatically
    date_mapping = {'Created': 'Created', 'Resolved': 'Resolved', 'created_at': 'Created', 'resolved_at': 'Resolved'}
    for col in df.columns:
        if col in date_mapping:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # 2. Apply Deep Subcategory Analysis
    if 'Short description' in df.columns:
        df['Deep_Subcategory'] = df['Short description'].apply(deep_infra_analysis)

    # --- KPI Overview ---
    st.divider()
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Incidents", f"{len(df):,}")
    
    if 'Assignment group' in df.columns:
        kpi2.metric("Unique Assignment Groups", df['Assignment group'].nunique())
    
    if 'Created' in df.columns and 'Resolved' in df.columns:
        df['MTTR_Hrs'] = (df['Resolved'] - df['Created']).dt.total_seconds() / 3600
        avg_mttr = df['MTTR_Hrs'].mean()
        kpi3.metric("Avg MTTR (Hours)", f"{avg_mttr:.2f}")

    # --- Analysis Tabs ---
    tab1, tab2, tab3 = st.tabs(["📊 Category Analysis", "📅 Monthly Trends", "🏢 Group Performance"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Top 100 Categories")
            # Uses 'Category' column if it exists, otherwise looks at the first few columns
            cat_col = 'Category' if 'Category' in df.columns else df.columns[1]
            st.dataframe(df[cat_col].value_counts().head(100), use_container_width=True)
        
        with c2:
            st.subheader("Deep Subcategory Breakdown")
            if 'Deep_Subcategory' in df.columns:
                sub_counts = df['Deep_Subcategory'].value_counts().reset_index()
                fig_sub = px.bar(sub_counts, x='count', y='Deep_Subcategory', orientation='h', 
                                 title="Analysis of Short Descriptions", color='count')
                st.plotly_chart(fig_sub, use_container_width=True)

    with tab2:
        st.subheader("Incident Volume (Month-on-Month)")
        if 'Created' in df.columns:
            df['Month'] = df['Created'].dt.to_period('M').astype(str)
            monthly_data = df.groupby('Month').size().reset_index(name='Volume')
            fig_line = px.line(monthly_data, x='Month', y='Volume', markers=True)
            st.plotly_chart(fig_line, use_container_width=True)

    with tab3:
        st.subheader("Top 20 Assignment Groups")
        if 'Assignment group' in df.columns:
            group_data = df['Assignment group'].value_counts().head(20).reset_index()
            group_data.columns = ['Group', 'Count']
            fig_groups = px.bar(group_data, x='Count', y='Group', orientation='h', color='Count')
            st.plotly_chart(fig_groups, use_container_width=True)

    # --- Search & Export ---
    st.divider()
    with st.expander("🔍 Search Full Infrastructure Dump"):
        search_query = st.text_input("Search Short Description (e.g. 'Link down')")
        if search_query:
            filtered_df = df[df['Short description'].str.contains(search_query, case=False, na=False)]
            st.write(f"Showing {len(filtered_df)} results:")
            st.dataframe(filtered_df)
        else:
            st.dataframe(df.head(500))

else:
    st.info("Please upload an Excel or CSV file to begin analysis.")

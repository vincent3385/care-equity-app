import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- UI CONFIG & VIBRANT STYLING ---
st.set_page_config(page_title="Care Equity AI", layout="wide", page_icon="🧬")

# Custom CSS for a colorful, modern "Consumer Service" look
st.markdown("""
    <style>
    .stApp { background: linear-gradient(to right, #f8f9fa, #e9ecef); }
    [data-testid="stMetricValue"] { color: #4361ee; font-weight: 700; }
    .stButton>button { 
        background-color: #4361ee; color: white; border-radius: 20px; 
        border: none; padding: 10px 24px; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #3f37c9; transform: scale(1.05); }
    .help-card { 
        background-color: #ff4d6d; color: white; padding: 20px; 
        border-radius: 15px; border-left: 5px solid #800f2f;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PERSISTENT DATA ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "task": "Pharmacy Pickup", "member": "Vincent", "status": "Done", "mins": 30, "type": "Errand"},
        {"id": 2, "task": "Hospital Trip", "member": "Sibling", "status": "Todo", "mins": 120, "type": "Medical"}
    ]

# --- APP HEADER ---
st.title("🧬 Care Equity Intelligence")
st.markdown("### *Balancing caregiving responsibilities automatically.*")

# --- TOP ROW: INSIGHTS & BURNOUT ALERTS ---
col1, col2, col3 = st.columns([1, 1, 1])

# Calculate share for the "Burnout Alert" (Competition Requirement)
df = pd.DataFrame(st.session_state.tasks)
vincent_share = (df[df['member'] == 'Vincent']['mins'].sum() / df['mins'].sum()) * 100

with col1:
    st.metric("Family Care Equity Score", "82/100", delta="+4%")
with col2:
    st.metric("Vincent's Workload", f"{int(vincent_share)}%", delta="High Load", delta_color="inverse")
with col3:
    if vincent_share >= 70:
        st.error("🚨 **BURNOUT ALERT**: Vincent has handled 70% of tasks this month!")

st.divider()

# --- MAIN INTERFACE ---
left_col, right_col = st.columns([2, 1])

with left_col:
    st.subheader("📅 Shared Care Dashboard")
    # Display colorful dataframe
    st.dataframe(df.style.background_gradient(cmap='Blues', subset=['mins']), 
                 use_container_width=True, hide_index=True)
    
    # "Request Help" Button & Modal (Friend's Suggestion)
    st.markdown("---")
    st.subheader("🆘 Need a Hand?")
    help_col1, help_col2 = st.columns(2)
    
    with help_col1:
        if st.button("🚨 REQUEST EMERGENCY HELP"):
            st.toast("Emergency alerts sent to all family members!", icon="⚠️")
            
    with help_col2:
        with st.popover("➕ Request New Help Task"):
            new_title = st.selectbox("What do you need?", ["Groceries", "Pharmacy Pickup", "Hospital Trip", "Misc Errands"])
            new_mins = st.number_input("Est. Minutes", 15, 300, 30)
            if st.button("Post to Dashboard"):
                st.session_state.tasks.append({"id": len(df)+1, "task": new_title, "member": "Unassigned", "status": "Todo", "mins": new_mins, "type": "General"})
                st.success("Task posted! The Equity Engine will auto-assign soon.")
                st.rerun()

with right_col:
    st.subheader("📊 Workload Distribution")
    fig = px.pie(df, values='mins', names='member', hole=0.5,
                 color_discrete_sequence=px.colors.sequential.RdBu)
    fig.update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("**AI Insight**: Sibling has 5 hours of availability this week. Reassigning 'Hospital Trip' to balance equity.")

# --- FOOTER (Competition Branding) ---
st.caption("Care Equity MVP • Designed for the 2026 Stella Zhang New Venture Competition")
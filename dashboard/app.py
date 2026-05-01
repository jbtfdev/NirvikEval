import json
import pandas as pd
import streamlit as st
from collections import defaultdict

st.set_page_config(page_title="NirvikEval Dashboard", layout="wide")


@st.cache_data
def load_results(path="results/latest.json") -> pd.DataFrame:
    with open(path, "r") as f:
        data = json.load(f)

    dframe = pd.DataFrame(data)

    return dframe

df = load_results()
if df.empty:
    st.error("No data found in the results/latest.json")
    st.stop()


def compute_metrics(dataframe):
    pr = dataframe["passed"].mean()
    avgs = dataframe["total_steps"].mean()
    tr = dataframe["timed_out"].mean()

    return pr, avgs, tr

#panel 1
pass_rate, avg_steps, timeout_rate = compute_metrics(df)

col1, col2, col3 = st.columns(3)
col1.metric("pass rate", f"{pass_rate:1%}")
col2.metric("average steps", f"{avg_steps:1f}")
col3.metric("timeout rate ", f"{timeout_rate:1%}")

#panel 2
st.subheader("Pass Rate by Category")

if "category" in df.columns:
    category_perf  = df.groupby("category")["passed"].mean()
    st.bar_chart(category_perf)
else:
    st.warning("Column 'category' not found in data")


def compute_tool_usage(dataframe):
    usage = defaultdict(lambda: defaultdict(int))

    for _,row in dataframe.iterrows():
        category = row.get("category", "unknown")
        steps = row.get("steps", [])

        for step in steps:
            tool = step.get("tool_name")
            if tool:
                usage[category][tool] += 1

    return pd.DataFrame(usage).fillna(0).astype(int)

st.subheader("Tool Usage by Category")

try:
    tool_usage_df = compute_tool_usage(df)
    st.dataframe(tool_usage_df)
except Exception as e:
    st.error(f"Error computing tool usage  : {e}")

st.subheader("Trace Explorer")
if "task_id" in df.columns:
    selected_task = st.selectbox("Select Task", df["task_id"])

    row = df[df["task_id"] == selected_task].iloc[0]

    st.markdown("### Task")
    st.write(row.get("task", "N/A"))

    st.markdown("### Final Answer")
    st.write(row.get("final_answer", "N/A"))

    st.markdown("### Steps")

    steps = row.get("steps", [])

    if not steps:
        st.warning("No steps found for this task")
    else:
        for step in steps:
            st.markdown(f"""
            **Step {step.get('step', 'N/A')}**

            - **Thought:** {step.get('thought', 'N/A')}
            - **Tool:** {step.get('tool_name', 'N/A')}
            - **Input:** {step.get('tool_input', 'N/A')}
            - **Output:** {step.get('tool_output', 'N/A')}
            - **Latency:** {step.get('latency_ms', 'N/A')} ms
            """)
else:
     st.warning("Column 'task_id' not found in data.")


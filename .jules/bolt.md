## 2025-05-18 - Avoid Repeated DataFrame Filtering in Streamlit Metric Loops
**Learning:** In Streamlit apps that re-render on every widget interaction, filtering large DataFrames (`df[df['col'] == val]`) inside UI display loops (e.g., rendering `st.metric` for N items) adds high CPU overhead per rerun.
**Action:** Extract filtered data into indexed dictionaries (`set_index('key')['val'].to_dict()`) prior to UI loops for O(1) dictionary lookups across reruns.

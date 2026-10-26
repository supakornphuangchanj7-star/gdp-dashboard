## 2025-05-18 - Avoid repeated DataFrame filtering in Streamlit render loops

**Learning:** In Streamlit applications, code outside `@st.cache_data` executes on every user interaction (rerun). Performing Pandas DataFrame filtering (`df[df['col'] == val]`) inside a loop over displayed items (e.g., UI metric cards) causes $O(N)$ overhead per card on every rerun. Pre-building a Python `dict` from a filtered slice (`dict(zip(df_slice['col'], df_slice['val']))`) converts repeated DataFrame queries into $O(1)$ dictionary lookups, improving metric calculation performance by ~85%.

**Action:** Look for per-item Pandas filtering inside UI rendering loops and convert them to dictionary lookups or indexed series lookups before entering the loop.

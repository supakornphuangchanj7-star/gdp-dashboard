## 2026-10-08 - O(N) DataFrame filtering in Streamlit render loop

**Learning:** In Streamlit apps that re-render top-to-bottom on interaction, executing repeated pandas DataFrame filtering (e.g. `df[df['Country Code'] == code]['GDP'].iat[0]`) inside loops scales poorly (O(N) search per item). Pre-indexing or converting yearly DataFrames to Python dictionaries (`dict(zip(df['Key'], df['Val']))`) before rendering loops provides O(1) lookups and ~6x speedup.

**Action:** When calculating metrics inside UI component render loops, always convert lookup DataFrames to dict mappings once outside the loop.

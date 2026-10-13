# Bolt's Journal

## 2026-03-30 - Pre-index DataFrame lookups before Streamlit metric rendering loops
**Learning:** Filtering Pandas DataFrames inside UI loops (`df[df['col'] == val]['target'].iat[0]`) causes linear scanning and DataFrame allocation on every rendered metric element during Streamlit reruns.
**Action:** Convert sliced DataFrame columns to Python dicts (`dict(zip(df['key'], df['val']))`) before entering rendering loops for O(1) lookups and ~8x faster loop execution.

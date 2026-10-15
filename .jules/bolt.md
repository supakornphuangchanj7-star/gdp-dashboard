## 2025-05-18 - Avoid repeated DataFrame boolean indexing inside Streamlit render loops

**Learning:** In Streamlit applications, every user interaction triggers a script re-render. Filtering a DataFrame with `df[df['col'] == val]` inside a loop (e.g., iterating over selected user choices to display metrics) performs $O(N)$ boolean mask operations per iteration. Pre-building dictionary mappings using `dict(zip(df['key'], df['val']))` outside the loop reduces lookups to $O(1)$ dictionary accesses, resulting in a ~13x speedup (~1.17ms vs ~15.3ms per rerun).

**Action:** Whenever iterating over user-selected keys to extract values from a DataFrame during render, pre-index or convert the DataFrame slice to a Python dictionary first.

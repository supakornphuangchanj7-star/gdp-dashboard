## 2026-03-30 - Pre-index DataFrames before per-country iteration
**Learning:** Repeatedly filtering DataFrames with boolean masks inside Streamlit loops (`df[df['Country Code'] == country]`) causes unnecessary allocation and linear scans ($O(N \cdot M)$). Pre-indexing into a Series with `set_index('Country Code')['GDP']` allows $O(1)$ dictionary-like lookups via `.get()`.
**Action:** Always pre-index DataFrames by key before iterating over user selections in Streamlit render loops.

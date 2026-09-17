## 2025-02-20 - Avoid DataFrame Filtering in Streamlit Render Loops

**Learning:** Linear DataFrame filtering operations like `df[df['col'] == val]` inside UI rendering loops (such as metric cards in Streamlit) execute on every rerun. When filtering across multiple countries or items, this scales linearly with the number of UI elements and full dataset size (O(N * M)), causing noticeable latency spikes on user interactions.

**Action:** Pre-filter datasets and build dictionary lookup tables (`dict(zip(key_series, val_series))`) outside of rendering loops to achieve O(1) lookups during UI iteration.

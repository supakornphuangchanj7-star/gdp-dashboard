## 2026-03-31 - Streamlit Rerun Loop Optimization
**Learning:** In Streamlit applications that execute top-to-bottom on every user interaction, doing repeated DataFrame boolean filtering (`df[df['col'] == val]`) inside loop renderings creates significant O(N * M) overhead (~10ms per rerun for 6 items).
**Action:** Extract filtered data subsets once into indexed Series or dictionary lookup maps before entering display loops to reduce per-rerun calculation time to ~2.8ms (~3.5x speedup).

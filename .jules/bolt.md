# Bolt's Journal - Critical Learnings Only

## 2026-11-10 - Pre-indexing filtered Streamlit DataFrames for metric rendering
**Learning:** In Streamlit apps that render multiple summary metrics inside a loop, performing repeated boolean filtering (`df[df['col'] == val]['target'].iat[0]`) on the full un-indexed DataFrame causes $O(K \times N)$ scans on every script rerun. For this 16,000+ row dataset, doing `filtered_df[filtered_df['Year'] == target_year].set_index('Country Code')['GDP']` prior to the loop dropped metric evaluation time from ~8.86ms to ~2.15ms (~75% reduction) and down from ~65.6ms to ~2.35ms when viewing 50+ countries.
**Action:** When computing summary cards/metrics in Streamlit loops, always pre-filter and index the subset DataFrame by the grouping/entity key before iterating to enable $O(1)$ lookups instead of repeated full-table scans.

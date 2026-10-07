## 2026-03-31 - Indexed Lookups vs. Repeated DataFrame Boolean Filtering in Loops

**Learning:** In pandas DataFrames representing time-series metrics per entity (e.g., `gdp_df`), filtering the DataFrame inside an entity iteration loop (`df[df['Country Code'] == country]['GDP'].iat[0]`) repeatedly creates boolean Series masks and scans the DataFrame for every iteration. Setting the entity identifier as the Index on single-year slice Series (`df[df['Year'] == year].set_index('Country Code')['GDP']`) enables O(1) hash lookups (`series.loc[country]`).
**Action:** Always index single-year metric Series by entity key before looping over selected entities to avoid O(N_countries * N_rows) repeated filtering overhead.

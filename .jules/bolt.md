## 2024-10-14 - Pre-slice DataFrame lookups in Streamlit render loops
**Learning:** Performing linear pandas DataFrame filtering (`df[df['col'] == val]`) inside a loop on every Streamlit script rerun is a major bottleneck because each filtering operation creates temporary DataFrames. Pre-slicing the data into dictionary lookups (`dict(zip(df['key'], df['val']))`) converts linear searches into $O(1)$ lookups, reducing rerun time by over 4x.
**Action:** When calculating metrics in a Streamlit loop across multiple items, pre-extract key-value dictionaries before entering the loop.

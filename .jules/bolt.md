## 2026-03-31 - Pandas linear filtering in UI render loops
**Learning:** Repeatedly filtering Pandas DataFrames inside UI loops (`df[df['col'] == val]`) introduces linear $O(N)$ filtering overhead per element, slowing down page reruns in Streamlit.
**Action:** Convert subset series or DataFrames to dictionaries (`set_index('key')['val'].to_dict()`) outside of loops for $O(1)$ constant-time lookup during UI rendering.

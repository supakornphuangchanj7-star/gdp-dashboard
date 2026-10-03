## 2025-05-18 - Pandas linear filtering vs Hash map lookups in loop rendering

**Learning:** Filtering a Pandas DataFrame repeatedly with boolean masks inside loop iterations (e.g. for UI element rendering in Streamlit) creates substantial overhead due to repeated DataFrame indexing and memory allocation.
**Action:** When calculating metrics for multiple items in a UI loop, pre-filter the subset once into a tuple/dict lookup map `(item_id, key) -> value` before the loop to achieve O(1) hash map lookups.

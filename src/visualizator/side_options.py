import streamlit

# Define options in sidebar
def options(st, len_iterations, key, value=0):
    id_iteration = st.sidebar.slider(
        label="Iteração",
        min_value=0,
        max_value=len_iterations,
        step=1,
        value=value,
        key=key)
    return id_iteration    

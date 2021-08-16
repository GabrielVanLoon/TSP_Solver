import streamlit

# Define options in sidebar
def options(st, len_iterations):
    id_iteration = st.sidebar.slider(
        label="Iteração",
        min_value=0,
        max_value=len_iterations,
        step=1,
        value=0)
    return id_iteration    
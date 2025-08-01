import streamlit as st
import pandas as pd
import numpy as np
from collections import Counter

# Calcular NNC
def compute_nnc(df, author_id):
    nic_list, n_list, N_list, nc_list = [], [], [], []
    for _, row in df.iterrows():
        authors_ids = [aid.strip() for aid in str(row["Author(s) ID"]).split(";") if aid.strip()]
        N = len(authors_ids)
        try:
            n = authors_ids.index(author_id) + 1
        except ValueError:
            n = np.nan
        try:
            NC = int(row["Cited by"])
        except:
            NC = 0
        SUM = sum([2**(-i) for i in range(1, N+1)])
        NNC = NC * (2 - SUM) / (2**n) if not np.isnan(n) else 0
        nic_list.append(NNC)
        n_list.append(n)
        N_list.append(N)
        nc_list.append(NC)
    df["NC"] = nc_list
    df["n"] = n_list
    df["N"] = N_list
    df["NNC"] = nic_list
    return df

# Detectar autor más frecuente
def detect_main_author(df):
    id_lists = df["Author(s) ID"].dropna().apply(lambda x: [aid.strip() for aid in x.split(";")])
    name_lists = df["Author full names"].dropna().apply(lambda x: [name.strip() for name in x.split(";")])
    all_ids = [aid for sublist in id_lists for aid in sublist]
    all_names = [name for sublist in name_lists for name in sublist]
    id_counts = Counter(all_ids)
    main_id = id_counts.most_common(1)[0][0]
    id_name_map = dict(zip(all_ids, all_names))
    main_name = id_name_map.get(main_id, "Nombre desconocido")
    return main_id, main_name

# Interfaz Streamlit
st.title("Calculadora de NNC (Número Normalizado de Citas)")

st.markdown("""
**¿Qué es el NNC?**

El Número Normalizado de Citas (**NNC**) mide la contribución de un autor a cada publicación en función de su posición en la lista de autores y el número total de autores.
""")

st.latex(r"NNC = \frac{NC \cdot (2 - \sum_{i=1}^{N} 2^{-i})}{2^n}")

st.markdown("""
Donde:
- `NC`: número de citas del artículo
- `n`: posición del autor en la lista
- `N`: número total de autores
""")

uploaded_files = st.file_uploader("Sube uno o más archivos CSV exportados desde un author profile de Scopus ('export all')", type="csv", accept_multiple_files=True)

summary_data = []
last_df_result = None

if uploaded_files:
    for uploaded_file in uploaded_files:
        uploaded_file.seek(0)
        df = pd.read_csv(uploaded_file)
        if not {"Author(s) ID", "Author full names", "Cited by", "Title"}.issubset(df.columns):
            st.warning(f"El archivo {uploaded_file.name} no tiene las columnas necesarias.")
            continue
        main_author_id, main_author_name = detect_main_author(df)
        df_result = compute_nnc(df, main_author_id)
        total_nc = df_result["NC"].sum()
        total_nnc = df_result["NNC"].sum()
        summary_data.append({
            "Autor": main_author_name.split(" (")[0],
            "ID": main_author_id,
            "Citas (Scopus)": total_nc,
            "NNC total": round(total_nnc, 3)
        })
        last_df_result = df_result[["Title", "NC", "n", "N", "NNC"]].sort_values(by="NNC", ascending=False)

    if summary_data:
        st.subheader("Resumen comparativo")
        st.dataframe(pd.DataFrame(summary_data).set_index("Autor").T)

    if last_df_result is not None:
        st.subheader("Resultados por publicación (último archivo)")
        st.dataframe(last_df_result)
        csv = last_df_result.to_csv(index=False)
        st.download_button(
            label="Descargar resultados como CSV",
            data=csv,
            file_name="author_nnc_results.csv",
            mime="text/csv"
        )


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Настройка страницы
st.set_page_config(
    page_title="CSV Analyzer",
    page_icon="📊",
    layout="wide"
)

# Кешированная загрузка данных
@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        try:
            # Попробовать прочитать как CSV
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            st.error(f"Ошибка при чтении файла: {e}")
            return None
    return None

# Заголовок
st.title("Анализ CSV‑файла")

# Загрузка файла
uploaded_file = st.file_uploader(
    "Загрузите CSV‑файл",
    type=["csv"],
    help="Выберите CSV‑файл для анализа"
)

if uploaded_file is not None:
    # Загрузка данных с кешированием
    df = load_data(uploaded_file)
    
    if df is not None:
        st.success("Файл успешно загружен!")
        
        # Отображение таблицы
        st.subheader("Содержимое файла")
        st.dataframe(df, height=400)
        
        # Информация о данных
        st.write("**Информация о наборе данных:**")
        st.write(f"- Количество строк: {df.shape[0]}")
        st.write(f"- Количество столбцов: {df.shape[1]}")
        st.write(f"- Типы данных: {dict(df.dtypes)}")
        
        # Выбор столбцов
        all_columns = df.columns.tolist()
        
        # Статистический анализ одного столбца
        st.subheader("Статистический анализ столбца")
        selected_col = st.selectbox(
            "Выберите столбец для анализа",
            all_columns,
            key="stat_col"
        )
        
        if selected_col:
            col_data = df[selected_col]
            
            # Фильтрация только числовых данных для статистики
            if pd.api.types.is_numeric_dtype(col_data):
                mean_val = col_data.mean()
                median_val = col_data.median()
                std_val = col_data.std()
                
                st.write(f"**Среднее:** {mean_val:.4f}")
                st.write(f"**Медиана:** {median_val:.4f}")
                st.write(f"**Среднеквадратичное отклонение:** {std_val:.4f}")
            else:
                st.warning("Для этого столбца статистика не рассчитывается (не числовой тип).")
        
        
        # Построение графиков для пар столбцов
        st.subheader("Визуализация данных")
        col1, col2 = st.columns(2)
        
        with col1:
            x_col = st.selectbox("Ось X", all_columns, key="x_col")
        with col2:
            y_col = st.selectbox("Ось Y", all_columns, key="y_col")
        
        chart_type = st.radio(
            "Тип графика",
            ["Линейный график", "Диаграмма рассеяния", "Столбчатая диаграмма"],
            key="chart_type"
        )
        
        # Создание графика
        fig, ax = plt.subplots(figsize=(10, 6))
        
        try:
            if chart_type == "Линейный график":
                ax.plot(df[x_col], df[y_col], marker='o')
                ax.set_title(f"Линейный график: {x_col} vs {y_col}")
            elif chart_type == "Диаграмма рассеяния":
                ax.scatter(df[x_col], df[y_col])
                ax.set_title(f"Диаграмма рассеяния: {x_col} vs {y_col}")
            elif chart_type == "Столбчатая диаграмма":
                # Для категориальных X берём среднее Y по группам
                grouped = df.groupby(x_col)[y_col].mean()
                grouped.plot(kind='bar', ax=ax)
                ax.set_title(f"Столбчатая диаграмма: среднее {y_col} по {x_col}")
            
            
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Ошибка при построении графика: {e}")
        
        
        # Статистика и графики распределения для выбранного столбца
        st.subheader("Распределение выбранного столбца")
        dist_col = st.selectbox(
            "Выберите столбец для анализа распределения",
            all_columns,
            key="dist_col"
        )
        
        fig2, ax2 = plt.subplots(1, 2, figsize=(14, 6))
        
        col_data = df[dist_col]
        
        # Гистограмма / кривая плотности
        if pd.api.types.is_numeric_dtype(col_data):
            sns.histplot(col_data, kde=True, ax=ax2[0])
            ax2[0].set_title(f"Гистограмма и KDE: {dist_col}")
            
            sns.boxplot(y=col_data, ax=ax2[1])
            ax2[1].set_title(f"Boxplot: {dist_col}")
        else:
            # Для категориальных — столбчатая диаграмма частот
            col_data.value_counts().plot(kind='bar', ax=ax2[0])
            ax2[0].set_title(f"Частота значений: {dist_col}")
            ax2[1].axis('off')  # Убираем второй подграфик
        
        st.pyplot(fig2)
        
        # Кнопка загрузки графика
        st.subheader("Скачать построенный график")
        if st.button("Сохранить текущий график"):
            # Сохраняем последний построенный график (fig)
            buf = StringIO()
            fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
            buf.seek(0)
            st.download_button(
                label="Скачать график как PNG",
                data=buf,
                file_name="plot.png",
                mime="image/png"
            )
else:
    st.info("Пожалуйста, загрузите CSV‑файл для начала анализа.")
import pandas as pd
import streamlit as st
import ast
import base64

def main():
    st.set_page_config(page_title="CSV 数据清洗", layout="wide")
    st.title("CSV 数据清洗")

    # 允许用户上传 CSV 文件
    uploaded_file = st.sidebar.file_uploader("上传 CSV 文件", type=['csv'])

    if uploaded_file is not None:
        # 读取上传的 CSV 文件
        df = pd.read_csv(uploaded_file)
        original_df = df.copy()

        # 重命名列
        st.sidebar.subheader("重命名列")
        renamed_columns = st.session_state.get("renamed_columns", {})

        rename_columns_container = st.sidebar.container()

        for column in df.columns:
            if column in renamed_columns:
                current_new_name = renamed_columns[column]
            else:
                current_new_name = column

            cols = rename_columns_container.columns(2)
            cols[0].write(column)
            new_column_name = cols[1].text_input("", current_new_name, key=f"rename_{column}")
            renamed_columns[column] = new_column_name
            st.session_state["renamed_columns"] = renamed_columns
            df = df.rename(columns=renamed_columns)

        # 筛选功能
        st.subheader("筛选数据")
        filter_conditions = []

        filter_col_layout = st.columns(3)

        for i in range(3):
            col_name = filter_col_layout[i].selectbox(f"选择第 {i + 1} 个筛选条件的列名", options=df.columns, key=f"filter_col_{i}")
            filter_option = filter_col_layout[i].selectbox(f"选择 {col_name} 的筛选条件", options=['无', '范围', '具体值'], key=f"filter_option_{i}")
            if filter_option == '范围':
                condition = filter_col_layout[i].text_input(f"输入 {col_name} 的范围（例如：(10, 20]）", key=f"range_{i}")
            elif filter_option == '具体值':
                condition = filter_col_layout[i].text_input(f"输入 {col_name} 的具体值", key=f"value_{i}")
            else:
                condition = None
            filter_conditions.append((col_name, filter_option, condition))

        # 提交筛选条件和复原按钮
        filter_button, reset = st.columns(2)
        submitted = filter_button.button("筛选")
        reset = reset.button("复原数据")

        if submitted:
            filtered_df = df.copy()

            for col, option, condition in filter_conditions:
                if option == '范围' and condition:
                    try:
                        lower, upper = ast.literal_eval(condition)
                        if isinstance(lower, (int, float)) and isinstance(upper, (int, float)):
                            filtered_df = filtered_df[(filtered_df[col] > lower) & (filtered_df[col] <= upper)]
                    except (ValueError, TypeError, SyntaxError):
                        st.error(f"无法解析 {col} 的范围: {condition}")
                elif option == '具体值' and condition:
                    filtered_df = filtered_df[filtered_df[col] == condition]

            st.write("符合条件的数据：")
            st.write(filtered_df)

            # 删除选中的数据
            delete_rows = st.button("删除筛选出的数据")
            if delete_rows:
                df = df.drop(filtered_df.index)
                st.write("删除后的数据：")
                st.write(df)

        if reset:
            df = original_df.copy()
            st.session_state["renamed_columns"] = {}
            st.write("已复原的原始数据：")
            st.write(df)
        else:
            st.write("完整数据：")
            st.write(df)

        # 导出数据
        if st.sidebar.button("导出数据"):
            csv = df.to_csv(index=False)
            b64 = base64.b64encode(csv.encode()).decode()  # 对数据进行编码
            href = f'<a href="data:file/csv;base64,{b64}" download="cleaned_data.csv">下载清洗后的 CSV 文件</a>'
            st.sidebar.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()

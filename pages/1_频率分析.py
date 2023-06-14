import streamlit as st
import pandas as pd
import plotly.express as px

def load_data(file):
    return pd.read_csv(file)

def visualize_data(column, chart_type, data):
    freq = data[column].value_counts()
    percent = round((freq / len(data)) * 100, 2)  # 保留两位小数的百分比形式

    # 创建新的 DataFrame，包含频次和百分比
    summary_df = pd.DataFrame({'频次': freq, '百分比': percent})
    summary_df.reset_index(inplace=True)
    summary_df.rename(columns={'index': column}, inplace=True)  

    # 使用 Streamlit 的 st.table() 函数显示表格
    st.table(summary_df)

    if chart_type == "柱状图":
        fig = px.bar(summary_df, x=column, y='百分比')  # 使用列名替换 '选项'
        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    elif chart_type == "条形图":
        fig = px.bar(summary_df, x='百分比', y=column, orientation='h')  # 使用列名替换 '选项'
        fig.update_traces(texttemplate='%{x:.2f}%', textposition='outside')
    else:
        fig = px.pie(summary_df, names=column, values='百分比')  # 使用列名替换 '选项'

    fig.update_layout(title=f"{column} 百分比")
    st.plotly_chart(fig)
    
def single_choice_analysis(data):
    column = st.selectbox("选择要分析的列", data.columns)
    chart_type = st.selectbox("选择图表类型", ["柱状图", "条形图", "饼图"])
    visualize_data(column, chart_type, data)

def multiple_choice_analysis(data):
    selected_columns = st.multiselect("选择多个变量", data.columns)
    new_column_name = st.text_input("为新的多重响应集命名")
    
    if st.button("创建多重响应集"):
        if new_column_name != "":
            data[new_column_name] = data[selected_columns].sum(axis=1)
            st.write(f"已创建 '{new_column_name}' 多重响应集")
            st.write(data.head())
        else:
            st.warning("请输入有效的名称")

    if new_column_name in data.columns:
        chart_type = st.selectbox("选择图表类型", ["柱状图", "条形图", "饼图"])
        visualize_data(new_column_name, chart_type, data)

st.set_page_config(page_title="频率分析", layout="wide")
st.title("频率分析")

uploaded_file = st.sidebar.file_uploader("上传CSV文件")

if uploaded_file:
    data = load_data(uploaded_file)
    st.write("已加载数据集")
    question_type = st.sidebar.selectbox("选择题目类型", ["单选题", "多选题"])
    
    if question_type == "单选题":
        single_choice_analysis(data)
    else:
        multiple_choice_analysis(data)
else:
    st.warning("请上传你的CSV文件")

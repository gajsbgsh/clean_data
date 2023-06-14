#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 20:17:08 2023

@author: zhenhao
"""

import streamlit as st
import pandas as pd
import plotly.express as px

st.title('交叉分析')

uploaded_file = st.sidebar.file_uploader('上传CSV文件', type='csv')

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader('原始数据')
    st.write(df)

    # 选择列
    cols = st.multiselect('请选择要分析的列（最多3个）', df.columns)

    if len(cols) > 0:
        if len(cols) >= 2:
            cross_analysis = pd.crosstab(index=df[cols[0]], columns=[df[col] for col in cols[1:]])
            cross_analysis_percentage = cross_analysis.apply(lambda r: r / r.sum() * 100, axis=1)

            st.subheader('交叉分析')
            st.write(cross_analysis_percentage)

            if len(cols) == 2:
                # 画堆叠柱状图
                stacked_bar = px.bar(cross_analysis_percentage.reset_index(), x=cols[0], y=cross_analysis_percentage.columns,
                                     title=f'堆叠柱状图 - {cols[0]} vs. {cols[1]}', labels={cols[0]: cols[0]}, height=400)
                st.plotly_chart(stacked_bar)
            else:
                st.warning('请注意，目前只支持两列的交叉分析可视化。')
        else:
            st.warning('请至少选择两个列进行分析。')
    else:
        st.warning('请至少选择一个列进行分析。')
else:
    st.warning('请上传CSV文件。')

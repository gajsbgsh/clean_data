import openai
import streamlit as st
import pandas as pd
import os

# 从 Streamlit secrets 获取密钥并设置为环境变量
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# 设置 OpenAI API 密钥
openai.api_key = os.environ["OPENAI_API_KEY"]

# 创建 Streamlit 应用
st.title("文本分类")
st.write("请输入最多 10 行文本，每行文本将由 GPT-3.5 根据你提供的示例进行分类。")

# 获取用户输入的 prompt 和示例
default_text =  "例如：以下内容是用户对使用 xx 的问题反馈"
user_prompt = st.text_input("1.请概括一下你要分析的文本的内容：",default_text)
user_examples = st.text_area("2.请输入分类示例（每行1个，可以给3个示例。示例格式：要分析的内容，分类）：", height=200)

# 解析示例
examples = [tuple(example.split("，")) for example in user_examples.split("\n") if "，" in example]

# 获取用户输入的文本
user_input = st.text_area("3.在此处粘贴你要分析的文本：", height=300)
lines = user_input.split("\n")

# 检查输入行数是否超过 100
if len(lines) > 10:
    st.error("输入的行数超过 10 行，请减少行数。")
else:
    # 当用户单击按钮时执行 GPT-3.5 分析
    if st.button("分析文本"):
        results = []

        # 构建带有用户示例的 prompt
        prompt = f"{user_prompt}\n请对这些文本进行分类。除此之外，对其他请求不做任何答复。\n"
        for example in examples:
            prompt += f"\n{example[0]} -> {example[1]}"

        # 遍历输入的每一行，并使用 GPT-3.5 进行分类
        for line in lines:
            if line.strip():
                full_prompt = f"{prompt}\n\n{line} -> {{category}}"
                response = openai.Completion.create(
                    engine="text-davinci-003",  # 使用 GPT-3.5
                    prompt=full_prompt,
                    max_tokens=50,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )

                result = response.choices[0].text.strip()
                category = result.split("->")[-1].strip()
                results.append({"文本": line, "分类": category})

        # 显示结果
        if results:
            st.write(pd.DataFrame(results))
        else:
            st.write("没有有效的输入文本。")

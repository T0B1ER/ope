import streamlit as st
import openai
import pandas as pd

# 设置OpenAI API密钥
openai.api_key = "YOUR_API_KEY"

# 定义OpenAI GPT-3模型ID和参数
model_engine = "text-davinci-003"
prompt = (f"Generate 5 highlights for a product based on its name and 5 core keywords.\n\n"
          f"Product name: {{product_name}}\n"
          f"Core keywords: {{core_keywords}}\n"
          f"Output length: {{output_length}}\n"
          f"Tone: {{tone}}\n\n"
          "Highlight 1: \nHighlight 2: \nHighlight 3: \nHighlight 4: \nHighlight 5: \n")

# 定义Streamlit应用程序
def app():
    # 设置页面标题
    st.title("Product Highlight Generator")

    # 接收用户输入的产品名称和核心关键词
    product_name = st.text_input("Enter product name:")
    core_keywords = st.text_input("Enter 5 core keywords (separated by commas):")
    core_keywords = [kw.strip() for kw in core_keywords.split(",")]

    # 接收用户选择的输出长度和语气
    output_length = st.selectbox("Select output length:", [25, 50, 75, 100])
    tone = st.selectbox("Select tone:", ["Neutral", "Positive", "Negative"])

    # 根据用户输入和选择调用OpenAI GPT-3 API生成亮点
    if product_name and core_keywords:
        prompt_with_values = prompt.format(product_name=product_name,
                                           core_keywords=core_keywords,
                                           output_length=output_length,
                                           tone=tone.lower())
        response = openai.Completion.create(engine=model_engine,
                                            prompt=prompt_with_values,
                                            temperature=0.5,
                                            max_tokens=150)
        highlights = response.choices[0].text.strip().split("\n")

        # 显示生成的亮点
        for i, highlight in enumerate(highlights):
            st.write(f"Highlight {i+1}: {highlight.strip()}")

    # 创建一个DataFrame并将其保存到Excel文件中
    if st.button("Export to Excel"):
        data = {"Product name": [product_name],
                "Core keywords": [", ".join(core_keywords)],
                "Output length": [output_length],
                "Tone": [tone],
                "Highlight 1": [highlights[0].strip()],
                "Highlight 2": [highlights[1].strip()],
                "Highlight 3": [highlights[2].strip()],
                "Highlight 4": [highlights[3].strip()],
                "Highlight 5": [highlights[4].strip()]}
        df = pd.DataFrame.from_dict(data)
        df.to_excel("product_highlights.xlsx", index=False)

if __name__ == "__main__":
    app()

import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("Hello User! introduse my project! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    # Welcome!
    반갑습니다! 이제부터 ML에대하여 학습한 과정을 소개하겠습니다! 😎
    ### 자료는 어디서?
    - 케글 [Kaggle](https://www.kaggle.com/)
    - 딥러닝 홀로서기 [git](https://github.com/heartcored98/Standalone-DeepLearning)
    
    ### 놀러오세요! 저의 자료창고입니다.
    - GitHub [Geon's Git](https://github.com/Geon-05/workspace_streamlit)
"""
)
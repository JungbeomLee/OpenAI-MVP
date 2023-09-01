# First
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]  # openai api key 설정

st.title("📖 동화 생성기") # title 설정 ( Webpage의 header와 비슷한 역할 )

with st.form(key='my_form'): # form 생성
    st.write("아이의 정보를 입력해주세요") # form 제목
    gender = st.selectbox('성별', ('남자', '여자') ) # 성별 선택 드랍다운
    theme = st.text_input(label='주제') # 주제 입력  
    genre = st.text_input(label='장르') # 장르 입력 
    submit_button = st.form_submit_button(label='동화 생성하기!') # 제출 버튼


if submit_button: # 제출 버튼 클릭시 이벤트
    if gender == "" or theme == "" or genre == "": # 입력되지 않은 필드가 있다면 에러메시지 띄우고, 아니면 넘어감
        st.error("공백인 필드가 있습니다!")
    else: 
        # chat gpt api에 입력받은 변수를 기반으로 동화를 생성함
        with st.spinner('맞춤형 동화를 생성중입니다..'): # 리턴이 돌아올 때까지 로딩 스피너를 돌림
            res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{gender}아이를 위한 {theme} 주제, {genre} 장르의 동화하나 만들어줘",
                }

            ],
            ) 
            story = bytes(res["choices"][0]["message"]["content"], encoding='utf-8').decode('utf-8')   
            imgprom = openai.ChatCompletion.create( # 달리 프롬프트 작성을 위한 chatgpt api 호출
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"{story}동화의 메인 장면의 이미지를 만들게 최대 400글자의 영어 프롬프트로 만들어줘",
                }  

            ],
            )
            imgprom = bytes(imgprom["choices"][0]["message"]["content"], encoding='utf-8').decode('utf-8')        
            imgprom.replace("\n", "")
            imgprom = imgprom[:398]
            
            # 달리 api 호출
            img = openai.Image.create(
                prompt = imgprom,
                n=1,
            size="512x512",    
                )
            
            # 스토리 출력
            pages = story.split("\n")

            for i, page in enumerate(pages):
                st.header(f"{i + 1} 페이지")
                st.write(page)

            st.write("이야기의 끝입니다!")
            # 달리에서 받아온 이미지 출력 (리스폰스가 링크로 돌아옴)
            st.image(img["data"][0]["url"])


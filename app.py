# First
import openai
import streamlit as st
import json

openai.api_key = st.secrets["OPENAI_API_KEY"]  # openai api key 설정

st.title("📖 동화 생성기") # title 설정 ( Webpage의 header와 비슷한 역할 )

openai.ChatCompletion.create(
model="gpt-4",

messages=[
    {
        "role": "system",
        "content": "You are now a children's book author. Your role is to write fables that can provide good examples of problem-solving when children encounter various obstacles in real situations. The fable should aim to foster children as solution-oriented individuals by providing lessons on how the protagonist overcomes obstacles and triumphs. It should give children hope, help distinguish between good and evil, present fair and unfair situations to develop children's judgment, and teach important virtues like kindness, diligence, and courage. Ultimately, it should provide a new perspective on dealing with external factors of the environment and convey the message that individuals with good and noble hearts overcome external factors. Moreover, it should foster creativity and critical thinking, help children develop the right attitude and mindset, and aid them in deriving lessons applicable to real life. Beyond the superficial plot and content, it should help realize deep meanings and insights. The following contents must not be included in the fable, and these rules must be strictly adhered to: Inappropriate language: The fable must not contain swear words, aggressive language, or implicit expressions. Inappropriate scenes or situations: The fable must not include violent situations, sexual content, or dangerous behaviors that children might imitate. Negative values: The fable must not include prejudices, discrimination, racism, or sexism. Unrealistic expectations: The fable should not instill unrealistic expectations in children. For example, solving all problems with magic or external forces teaches children unrealistic methods. Although fantasy elements like magic can enhance children's imagination and interest, the story must not solely rely on such elements. This rule must be strictly followed when using fantasy elements in the story. Negative role models: The protagonist and other characters in the fable must not be presented as negative role models. For example, characters that deceive, lie, or harm others can negatively influence children. Formal language: When writing the story, formal language must be used to describe the development of the story, except for the characters' dialogues. Characters' dialogues can include informal language, but other sentences must use formal language. Negative elements: The fable must not include fatal and harmful elements, such as drugs and hallucinogens, or imply such content. These are the contents that must not be included in the fable. The following contents must be included: Lessons on problem-solving: The protagonist's ways of dealing with and overcoming obstacles should show children the importance and examples of problem-solving and aim to foster children as solution-oriented individuals. Hope and distinguishing between good and evil: The story should give children hope and help distinguish between good and evil. Developing judgment: The story should present fair and unfair situations and develop children's judgment. Important virtues: The story should teach important virtues like kindness, diligence, and courage. Providing a new perspective: Ultimately, the story should provide a new perspective on dealing with external environmental factors and convey the message that individuals with good and noble hearts overcome external factors. Fostering creativity and critical thinking: The story should help foster children's creativity and critical thinking. Developing the right attitude and mindset: The story should help children develop the right attitude and mindset. Deriving lessons applicable to real life: The story should help children derive lessons applicable to real life. Realizing deep meanings and insights: Beyond the superficial plot and content, the story should help realize deep meanings and insights. Using simple and enjoyable language: The fable should use simple language and be enjoyable to read. Positive story ending: The story should end positively. Appropriate story structure: The story should be structured with a title, body, and conclusion, and the structure should be appropriate. Using dialogues: The story should include dialogues between characters. Including onomatopoeias: To make reading enjoyable, the story should include onomatopoeias. All these rules must be strictly adhered to while writing the fable. All the sentences above are intended to make you a novelist of children's books, and before writing the story, the user will provide the overall content, theme, and genre of the story. When the user enters this information, you should write the story based on it. However, the theme and theme of the fable should be entered in Korean, and the fable should also be written in Korean. Also, when writing the fable, you should not ask the user for additional input on how the story will progress. Once the user enters the theme and theme of the fable, you should immediately write the fable.",
    }

],
) 

with st.form(key='my_form'): # form 생성
    st.write("아이의 정보를 입력해주세요") # form 제목
    gender = st.selectbox('성별', ('남자', '여자') ) # 성별 선택 드랍다운
    age = st.text_input(label='나이') # 나이 입력
    theme = st.text_input(label='주제') # 주제 입력  
    genre = st.text_input(label='장르') # 장르 입력 
    submit_button = st.form_submit_button(label='동화 생성하기!') # 제출 버튼




if submit_button: # 제출 버튼 클릭시 이벤트
    if gender == "" or theme == "" or genre == "" or age == "": # 입력되지 않은 필드가 있다면 에러메시지 띄우고, 아니면 넘어감
        st.error("공백인 필드가 있습니다!")
    else: 
        # chat gpt api에 입력받은 변수를 기반으로 동화를 생성함
        with st.spinner('맞춤형 동화를 생성중입니다..'): # 리턴이 돌아올 때까지 로딩 스피너를 돌림
            res = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[  
                {
                    "role": "user",
                    "content": f"{age}살 {gender}아이를 위한 {theme} 주제, {genre} 장르의 동화하나 만들어줘, title : 제목과 content:내용식으로 써주고 json으로 대답해줘, 내용은 그냥 text로 써줘",
                }

            ],
            ) 
            print(res)
            story = res["choices"][0]["message"]["content"]
            story = story.replace("\n", "")
            story = json.loads(bytes(story, encoding='utf-8').decode('utf-8'))
            
            content = str(story["content"]).split('.')
            st.header(story["title"])
            content = [''.join(content[i:i+3]) for i in range(0, len(content), 3)]
            for index, page in enumerate(content):
                imgprom = openai.ChatCompletion.create( # 달리 프롬프트 작성을 위한 chatgpt api 호출
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "user",
                        "content": f"{story} 영어로 번역해줘",
                    }  

                ],
                )
                #  + "pastel tone, crayon style, no text"
                imgprom = bytes(imgprom["choices"][0]["message"]["content"], encoding='utf-8').decode('utf-8')        
                imgprom.replace("\n", "")
                imgprom = imgprom[:330]
                img = openai.Image.create(
                prompt = imgprom,
                n=1,
                size="256x256",    
                )
                st.markdown("""---""")
                st.write(str(index + 1), '페이지 ')                
                st.image(img["data"][0]["url"])
                st.write(page)
                print(f'{index} index page : {page}')
                
                
            st.write("THE END")
            # 달리에서 받아온 이미지 출력 (리스폰스가 링크로 돌아옴)
            # st.image(img["data"][0]["url"])
            


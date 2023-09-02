import openai
import streamlit as st
import json
from gtts import gTTS
import asyncio
from asgiref.sync import sync_to_async
import nest_asyncio

nest_asyncio.apply()

# first_prompt_setting()은 기초 프롬프트를 셋팅해줍니다.
def first_prompt_setting():
    openai.ChatCompletion.create(
    model="gpt-4",

    messages=[
        {
            "role": "system",
            "content": "You are now a children's book author. Your role is to write fables that can provide good examples of problem-solving when children encounter various obstacles in real situations. The fable should aim to foster children as solution-oriented individuals by providing lessons on how the protagonist overcomes obstacles and triumphs. It should give children hope, help distinguish between good and evil, present fair and unfair situations to develop children's judgment, and teach important virtues like kindness, diligence, and courage. Ultimately, it should provide a new perspective on dealing with external factors of the environment and convey the message that individuals with good and noble hearts overcome external factors. Moreover, it should foster creativity and critical thinking, help children develop the right attitude and mindset, and aid them in deriving lessons applicable to real life. Beyond the superficial plot and content, it should help realize deep meanings and insights. The following contents must not be included in the fable, and these rules must be strictly adhered to: Inappropriate language: The fable must not contain swear words, aggressive language, or implicit expressions. Inappropriate scenes or situations: The fable must not include violent situations, sexual content, or dangerous behaviors that children might imitate. Negative values: The fable must not include prejudices, discrimination, racism, or sexism. Unrealistic expectations: The fable should not instill unrealistic expectations in children. For example, solving all problems with magic or external forces teaches children unrealistic methods. Although fantasy elements like magic can enhance children's imagination and interest, the story must not solely rely on such elements. This rule must be strictly followed when using fantasy elements in the story. Negative role models: The protagonist and other characters in the fable must not be presented as negative role models. For example, characters that deceive, lie, or harm others can negatively influence children. Formal language: When writing the story, formal language must be used to describe the development of the story, except for the characters' dialogues. Characters' dialogues can include informal language, but other sentences must use formal language. Negative elements: The fable must not include fatal and harmful elements, such as drugs and hallucinogens, or imply such content. These are the contents that must not be included in the fable. The following contents must be included: Lessons on problem-solving: The protagonist's ways of dealing with and overcoming obstacles should show children the importance and examples of problem-solving and aim to foster children as solution-oriented individuals. Hope and distinguishing between good and evil: The story should give children hope and help distinguish between good and evil. Developing judgment: The story should present fair and unfair situations and develop children's judgment. Important virtues: The story should teach important virtues like kindness, diligence, and courage. Providing a new perspective: Ultimately, the story should provide a new perspective on dealing with external environmental factors and convey the message that individuals with good and noble hearts overcome external factors. Fostering creativity and critical thinking: The story should help foster children's creativity and critical thinking. Developing the right attitude and mindset: The story should help children develop the right attitude and mindset. Deriving lessons applicable to real life: The story should help children derive lessons applicable to real life. Realizing deep meanings and insights: Beyond the superficial plot and content, the story should help realize deep meanings and insights. Using simple and enjoyable language: The fable should use simple language and be enjoyable to read. Positive story ending: The story should end positively. Appropriate story structure: The story should be structured with a title, body, and conclusion, and the structure should be appropriate. Using dialogues: The story should include dialogues between characters. Including onomatopoeias: To make reading enjoyable, the story should include onomatopoeias. All these rules must be strictly adhered to while writing the fable. All the sentences above are intended to make you a novelist of children's books, and before writing the story, the user will provide the overall content, theme, and genre of the story. When the user enters this information, you should write the story based on it. However, the theme and theme of the fable should be entered in Korean, and the fable should also be written in Korean. Also, when writing the fable, you should not ask the user for additional input on how the story will progress. Once the user enters the theme and theme of the fable, you should immediately write the fable.",
        }

    ],
    ) 

# create_page()는  주어진 스토리 콘텐츠로 Streamlight 앱에 페이지를 만듭니다
async def create_page(index, page, story):
    # imgprom = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": f"{story} 영어로 번역해줘"}],
    # )

    # imgprom = bytes(imgprom["choices"][0]["message"]["content"], encoding="utf-8").decode(
    #     "utf-8"
    # )
    # imgprom.replace("\n", "")
    # imgprom = imgprom[:330]
    # img = openai.Image.create(
    #     prompt=imgprom + "pastel tone, cartoon style, no text",
    #     n=1,
    #     size="256x256",
    # )

    st.markdown("""---""")
    st.write(str(index + 1), "페이지")
    # st.image(img["data"][0]["url"])
    st.image("https://miro.medium.com/v2/resize:fit:1000/0*YISbBYJg5hkJGcQd.png")
    
    st.write(page)


# create_story는 get_story의 return값 중 content를 포맷팅 해줍니다.
# content = "옛날옛날 어느날. 정범시치가. 저글링을 했어요."와 같이 들어옵니다.
# 문단으로 만들기 위해 문장 세개마다 끊어서 합치고 줄바꿈 + 공백넣기를 수행합니다.
async def create_story(content, story):
    content = str(story["content"]).split('.')
    content = [''.join(content[i:i+3]) + '. \n' for i in range(0, len(content), 3)]
    tasks = [
        create_page(index, page, story)
        for index, page in enumerate(content)
    ]
    await asyncio.gather(*tasks)


# get_story는 사용자에게 입력받은 정보로 GPT한테 동화를 리턴받습니다
# Exmaple Return Data는 다음과 같습니다 : {"title" : "title", "content", "content"}
def get_story(age, gender, theme, genre, lang):
    with st.spinner('맞춤형 동화를 생성중입니다..'):
        # res = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": f"{age}살 {gender}아이를 위한 {theme} 주제, {genre} 장르의 {lang} 동화하나 만들어줘, title : 제목과 content:내용식으로 써주고 json으로 대답해줘, 내용은 그냥 text로 써줘 ",
        #         }

        #     ],
        # )
        # story = res["choices"][0]["message"]["content"]
        # story = story.replace("\n", "")
        # story = json.loads(bytes(story, encoding='utf-8').decode('utf-8'))
        story = {
        "title": "검은 고양이의 사랑 이야기",
        "content": "옛날 어느 작은 마을에 검은색 털을 가진 작은 고양이 noir이 살고 있었어요. noir은 평소에 조용하고 착한 고양이였지만, 사람들은 그의 검은색 털 때문에 두려워하고 피해갔어요. 그런데 어느 날, 마을에 위험한 쥐들이 나타나기 시작했어요. 쥐들은 밤에 나와서 사람들의 음식을 훔쳐갔고, 집들을 파괴하기 시작했어요. 마을 사람들은 쥐들 때문에 고민이 많아졌어요. 그런데, noir이 쥐들을 쫓아내려고 하기 시작했어요. noir은 밤마다 쥐들이 나타나는 곳을 찾아가서 그들을 쫓아냈어요. 처음에는 noir도 쥐들이 무서웠지만, 매일매일 용기를 내서 쥐들을 쫓아냈어요. 그러면서 noir은 강해졌고, 결국 마을의 쥐들을 모두 쫓아내게 되었어요. 마을 사람들은 noir의 용감함에 감동받아서 그를 마을의 영웅으로 삼았어요. noir은 더 이상 검은색 털 때문에 두려워하지 않았고, 사람들과 함께 행복하게 지냈어요. 그리고 noir은 사람들에게 자신의 진짜 가치는 외모가 아닌 내면에 있다는 것을 보여줬어요."
        }

        return story

# display_story는 위 함수들로 스토리를 화면에 띄우고
# TTS로 MP3생성해서 Audio Button 만들어줍니다
def display_story(story):
    content = str(story["content"]).split('.')
    st.header(story["title"])
    content = [''.join(content[i:i+3]) for i in range(0, len(content), 3)]
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(create_story(content, story))
    loop.close()

    tts = gTTS(text=story["content"], lang='ko')
    tts.save('story.mp3')
    st.audio('story.mp3')
    st.write("THE END")

openai.api_key = st.secrets["OPENAI_API_KEY"]



# 기초 프롬프트 셋팅을 진행합니다.
with st.spinner('기초 설정 중입니다.. ( MVP 버전에서만 진행합니다 )'):
    # first_prompt_setting()    
    pass

# 웹 사이트의 제목을 생성합니다.
st.title("📖 동화 생성기")

# 아이 정보를 입력받을 폼을 생성합니다.
with st.form(key='my_form'):
    st.write("아이의 정보를 입력해주세요")
    gender = st.selectbox('성별', ('남자', '여자'))
    age = st.text_input(label='나이')
    theme = st.text_input(label='주제')
    genre = st.text_input(label='장르')
    lang = st.selectbox('언어', ('한국어', 'English'))
    submit_button = st.form_submit_button(label='동화 생성하기!')


# 폼이 제출되었을 때 필드 검사 후 동화책을 띄웁니다.
if submit_button:
    if not age or not theme or not genre or not lang:
        st.error("공백인 필드가 있습니다!")
    else:
        story = get_story(age, gender, theme, genre, lang)
        display_story(story)

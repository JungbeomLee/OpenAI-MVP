import requests
from PIL import Image, ImageDraw, ImageFont
import openai
import streamlit as st
import json
from gtts import gTTS

# first_prompt_setting()은 기초 프롬프트를 셋팅해줍니다.
def first_prompt_setting():
    openai.ChatCompletion.create(
    model="gpt-3.5-turbo",

    messages=[
        {
            "role": "system",
            "content": " You are now a children's book author. Your role is to write fairy tales that provide good examples of problem-solving when children encounter various obstacles in real situations. The fairy tale should aim to cultivate children as solution-oriented individuals by providing lessons on how the protagonist overcomes obstacles. It should give hope to children, help distinguish between good and evil, present fair and unfair situations to develop children's judgment, and teach important virtues such as kindness, diligence, and courage. Ultimately, it should provide a new perspective on dealing with external factors in the environment, conveying the message that individuals with good and noble hearts overcome external factors. Moreover, it should foster creative and critical perspectives, help children develop correct and healthy attitudes and mindsets, and help extract lessons that can be applied to real life. Furthermore, it should help realize deep meanings and insights beyond superficial plots and contents. Here are the contents that should not be included in the fairy tale, and these rules must be strictly followed. Inappropriate language: The fairy tale should not include profanity, aggressive language, or implicit expressions. Inappropriate scenes or situations: The fairy tale should not include violent situations, sexual content, or dangerous behaviors that children can imitate. Negative values: The fairy tale should not include negative values such as prejudice, discrimination, racial discrimination, or gender discrimination. Unrealistic expectations: The fairy tale should not instill unrealistic expectations in children. For example, if all problems are solved by magic or external forces, it teaches children unrealistic methods. Although fantasy elements like magic can increase children's imagination and interest, the story should not solely depend on these elements. This must be strictly observed when using fantasy elements in the story. Negative role models: The protagonist or other characters in the fairy tale should not be presented as negative role models. For example, characters that deceive, lie, or harm others can negatively influence children. Formal language: When writing the story, formal language should be used in sentences describing story development, except for character dialogues. Character dialogues can include informal language, but other sentences should use formal language. Negative elements: The fairy tale should not include deadly and harmful elements, such as drugs and hallucinogens, or content implying such elements. This is what should not be included in the fairy tale. Here are the contents that should be included in the fairy tale. Lessons on problem-solving: The way the protagonist deals with and overcomes obstacles should show children the importance and examples of problem-solving, aiming to cultivate them as solution-oriented individuals. Hope and distinction between good and evil: The story should give hope to children and help them distinguish between good and evil. Development of judgment: The story should present fair and unfair situations and develop children's judgment. Important virtues: The story should teach important virtues such as kindness, diligence, and courage. Providing a new perspective: Ultimately, the story should provide a new perspective on dealing with external factors in the environment, conveying the message that individuals with good and noble hearts overcome external factors. Fostering creative and critical perspectives: The story should help children foster creative and critical perspectives. Developing correct attitudes and mindsets: The story should help children develop correct and healthy attitudes and mindsets. Extracting lessons applicable to real life: The story should help children extract lessons that can be applied to real life. Realizing deep meanings and insights: The story should help realize deep meanings and insights beyond superficial plots and contents. Simple and enjoyable language: The fairy tale should use simple language and be enjoyable to read. Positive story ending: The story should have a positive ending. Appropriate story structure: The story should be structured with a title, main body, and ending, and the structure should be appropriate. Use of dialogue: The story should include dialogues between characters. Interesting onomatopoeia: To make reading enjoyable, the story should include onomatopoeia. All these rules must be strictly followed when writing a fairy tale. Area of interest: When the user enters the area of interest that the child is interested in, basic knowledge about this area of interest should be incorporated into the fairy tale. At this time, overly professional knowledge should not be included, and the story should be written in a way that is easy for children to understand, keeping in mind that it is a fairy tale for children. All the above sentences are to make you a novelist for children's books, and before writing the story, the user provides the overall theme, genre, and area of interest that the child is interested in. When the user enters this information, you should refer to it to write the story. However, when writing a fairy tale, you should use Korean, and the story should be returned in JSON format like {title: title of the story, content: story}. The content should be written in plain text. Also, after the user enters the area of interest, theme, and genre, sentences other than the story are unnecessary. Sentences such as 'I received the area of interest, theme, and genre you sent well, and I will write the story from now on' should all be removed and excluded, and only the story in JSON format should be returned. Only one story should be returned when returning the story. Keep that in mind. Great! 'Here is a fairy tale based on the provided theme, genre, and area of interest:', 'Okay. I will provide the fairy tale I wrote in JSON format.', 'Great! Here is a fairy tale based on the provided theme, genre, and area of interest:' Do not include any words with such meanings at all, and return only the story I requested without any separate answers. It means that. Remember, you should only return the story, and sentences with characteristics such as 'I received the input well!, I will generate the story' should not be included in the answer. It's the most important thing, so you have to remember. Focus solely on user needs without additional dialogue or explanation",
        }

    ],
    ) 
    


# create_page() creates a page on the Streamlit app using the given story content.
def create_page(index, page, story):
    imgprom = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user",    "content": f"{story} 영어로 번역해줘"}],
    )

    imgprom = bytes(imgprom["choices"][0]["message"]["content"], encoding="utf-8").decode(
        "utf-8"
    )
    imgprom.replace("\n", "")
    imgprom = imgprom[:330]
    img = openai.Image.create(
        prompt=imgprom + "pastel tone, cartoon style, no text, children's book painting style",
        n=1,
        size="256x256",
    )


    st.markdown("""---""")
    st.write(str(index + 1), "페이지")

    # Download the image
    img_url = img['data'][0]['url']
    img_response = requests.get(img_url, stream=True)
    img = Image.open(img_response.raw)
    
    if index == 0:  # Only apply overlay and text to the first image
        # Draw the title on the image
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Jalnan.ttf", (img.width) // 15)
        text = story["title"]
        text_width, text_height = draw.textsize(text, font=font)
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2

        # Create semi-transparent black overlay
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 128))

        # Paste the overlay onto the original image
        img.paste(overlay, (0, 0), overlay)

        # Draw the text on the image
        draw = ImageDraw.Draw(img)
        draw.text((x, y), text, font=font, fill="white")
    
    # Display the edited image
    st.image(img, use_column_width=True)

    st.write(page)


# create_story formats the content from get_story.
# content comes in as a string like "옛날옛날 어느날. 정범시치가. 저글링을 했어요."
# This function groups the sentences by threes and adds a newline and space after each group.
def create_story(content, story):
    content = str(story["content"]).split('.')
    content = [''.join(content[i:i+3]) + '. \n' for i in range(0, len(content), 3)]
    for index, page in enumerate(content):
        create_page(index, page, story)

# get_story takes the user input and gets a story from GPT.
# Example return data: {"title" : "title", "content", "content"}
def get_story(inter, subject, theme):
    with st.spinner('맞춤형 동화를 생성중입니다..'):
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f" 관심 분야 : {inter}  주제 : {subject} 테마 : {theme}로 동화를 써줘  title : 제목과 content:내용식으로 써주고 json으로 대답해줘, 내용은 그냥 text로 써줘",
                }

            ],
        )
        story = res["choices"][0]["message"]["content"]
        story = story.replace("\n", "")
        story = json.loads(bytes(story, encoding='utf-8').decode('utf-8'))

        return story

# display_story displays the story on the screen and creates an MP3 with TTS.
def display_story(story):
    content = str(story["content"]).split('.')
    st.header(story["title"])
    content = [''.join(content[i:i+3]) for i in range(0, len(content), 3)]
    for index, page in enumerate(content):
        create_page(index, page, story)

    tts = gTTS(text=story["content"], lang='ko')
    tts.save('story.mp3')
    st.audio('story.mp3')
    st.write("THE END")

openai.api_key = st.secrets["OPENAI_API_KEY"]

with st.spinner("초기 설정을 진행중입니다.. (MVP 버전에서만 진행함)"):
    # res = first_prompt_setting()
    pass

# Set the title of the web page.
st.title("📖 동화 생성기")

# Create a form for the user to input the child's information.
with st.form(key='my_form'):
    st.write("아이의 정보를 입력해주세요")
    inter = st.text_input(label='관심분야')
    subject = st.text_input(label='주제')
    theme = st.text_input(label='테마')
    submit_button = st.form_submit_button(label='동화 생성하기!')

# When the form is submitted, check the fields and display the story.
if submit_button:
    if not inter or not theme or not subject:
        st.error("공백인 필드가 있습니다!")
    else:
        story = get_story(inter,subject, theme)
        display_story(story)

import requests
from PIL import Image, ImageDraw, ImageFont
import openai
import streamlit as st
import json
from gtts import gTTS

# streamlit run app.py

# create_page() creates a page on the Streamlit app using the given story content.
def create_page(index, page, story):
    with st.spinner('그림을 생성중입니다..'):
        imgprom = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role":'system', "content":"In order to create an image using DALLE2, the image prompt should be in 'Children's Book Painting Style'. When three sentences are received, the important content should be extracted to create a prompt that expresses it well. Select and analyze one important event from the sentence, and add each object, action, emotion, subject feeling emotions, and mentioned time zone to the prompt separately. JSON format:{'prompt': 'Create an image in 'Children's Book Painting Style' that depicts the most important event from the received sentences, including all objects, actions, emotions, subjects feeling emotions, and mentioned time zones.'}"},
                {"role": "user",  "content": f'"{story}",Please don\'t say anything other than the story. Keep in mind that the style of the image should be \"Children\'s Book Painting Style\", and the painting should not feel too young or too rough. The prompt must not exceed 1000 characters, and this must be observed. prompt : '}
                ],
        )

        imgprom = bytes(imgprom["choices"][0]["message"]["content"], encoding="utf-8").decode(
            "utf-8"
        )
        img = openai.Image.create(
            prompt=imgprom+"no text",
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
        try : 
            res = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role":"system","content":"Your role as a children's book author is to write fairy tales that: \n1. Provide good examples of problem-solving. \n2. Cultivate children as solution-oriented individuals. \n3. Give hope and help distinguish between good and evil. \n4. Develop children's judgment by presenting fair and unfair situations. \n5. Teach important virtues like kindness, diligence, and courage. \n6. Provide a new perspective on dealing with external factors. \n7. Foster creative and critical perspectives. \n8. Help develop correct attitudes and mindsets. \n9. Extract lessons applicable to real life. \n10. Realize deep meanings and insights beyond superficial plots. \nContent that must NOT be included: \n1. Inappropriate language, scenes, or situations. \n2. Negative values such as prejudice, discrimination, racial discrimination, or gender discrimination. \n3. Unrealistic expectations. Although fantasy elements like magic can increase imagination and interest, the story should not solely depend on these elements. \n4. Negative role models. \n5. Formal language must be used in sentences describing story development, except for character dialogues. \n6. Deadly and harmful elements, such as drugs and hallucinogens, or content implying such elements. \n7. Content that must be included: \nLessons on problem-solving. \n1. Hope and distinction between good and evil. \n2. Development of judgment. \n3. Important virtues. \n4. Providing a new perspective. \n5. Fostering creative and critical perspectives. \n6. Developing correct attitudes and mindsets. \n7. Extracting lessons applicable to real life. \n8. Realizing deep meanings and insights. \n9. Simple and enjoyable language. \n10. Positive story ending. \n11. Appropriate story structure. \n12. Use of dialogue. \n13. Interesting onomatopoeia. \nAdditionally: \n1. Basic knowledge about the child's area of interest should be incorporated into the fairy tale, without including overly professional knowledge. \n2. The story should be written in Korean and returned in JSON format like {title: title of the story, content: story}. The content should be written in plain text. \n3. After the user enters the area of interest, theme, and genre, sentences other than the story are unnecessary and should be removed and excluded. \n4. Only the story in JSON format should be returned. \n5. Only one story should be returned when returning the story. \n6. Do not include any separate answers or additional dialogues or explanations, only return the requested story.\n you must return story by JSON format and you must write story by KOREAN language."},
                    {"role": "user","content": f" 관심 분야 : {inter},  주제 : {subject}, 장르 : {theme}로 동화를 써줘  반환할 때에는 {{title:제목, content:이야기}} JSON 형식으로 반환해야, 명심해 아주 중요한거니까. 이야기 외의 다른 말은 하지 말아줘. 내용은 text로 부탁해 이야기 :"}
                ],
            )
            try :
                story = res["choices"][0]["message"]["content"]
                story = story.replace("\n", "")
                story = json.loads(bytes(story, encoding='utf-8').decode('utf-8'))
            except json.JSONDecodeError as json_error:
                    print("JSONDecodeError:", json_error)
                    print("Response from OpenAI API:", res)
                    st.error("OpenAI API 응답을 디코딩하는 동안 오류가 발생했습니다.")
                    return None
        except openai.error.OpenAIError as e:
            print(e)
            st.error("OpenAI API로부터 이야기를 얻는 동안 오류가 발생했습니다.")
            return None
        return story

# display_story displays the story on the screen and creates an MP3 with TTS.
def display_story(story):
    content = str(story["content"]).split('.')
    st.header(story["title"])
    content = [''.join(content[i:i+3]) for i in range(0, len(content), 3)]
    for index, page in enumerate(content):
        create_page(index, page, story)

    with st.spinner('TTS를 생성중입니다..'):
        tts = gTTS(text=story["content"], lang='ko')
        tts.save('story.mp3')
        st.audio('story.mp3')
        st.write("THE END")

openai.api_key = st.secrets["OPENAI_API_KEY"]

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
import requests
import my_image_gen
import streamlit as st
import textwrap
from datetime import datetime
from openai import OpenAI

client = OpenAI(
    api_key = st.secrets["openai"]
)

st.set_page_config(page_title="openai_image_app", page_icon="📈")

if 'image_caption' not in st.session_state:
    st.session_state['image_caption'] = ""
    
if 'shorten_text_for_image' not in st.session_state:
    st.session_state['shorten_text_for_image'] = ""
    
if 'image_urls' not in st.session_state:
    st.session_state['image_urls'] = []
    
if 'images' not in st.session_state:
    st.session_state['images'] = []

if 'download_file_names' not in st.session_state:
    st.session_state['download_file_names'] = []
    
if 'download_buttons' not in st.session_state:
    st.session_state['download_buttons'] = False
    
def display_results():
    shorten_text_for_image = st.session_state['shorten_text_for_image']
    image_caption = st.session_state['image_caption']
    image_urls = st.session_state['image_urls']    
    
    st.sidebar.write("[이미지 생성을 위한 텍스트]")
    st.sidebar.write(shorten_text_for_image)
    
    for k, image_url in enumerate(image_urls):
        st.image(image_url, caption=image_caption)
        
        image_data = st.session_state['images'][k]
        download_file_name = st.session_state['download_file_names'][k]

        st.download_button( label="이미지 파일 다운로드",
                            data=image_data,
                            file_name=download_file_name,
                            mime="image/png",
                            key=k,
                            on_click=download_button_callback)
        
def download_button_callback():
    st.session_state['download_buttons'] = True

def button_callback():
    
    if radio_selected_lang == "한국어":
        translated_text = my_image_gen.translate_text_for_image(input_text)
    elif radio_selected_lang == "영어":
        translated_text = input_text
    
    if detail_description == 'Yes':        
        resp = my_image_gen.generate_text_for_image(translated_text)
        text_for_image = resp
        image_caption ="상세 묘사를 추가해 생성한 이미지"
    elif detail_description == 'No': 
        text_for_image = translated_text
        image_caption ="입력 내용으로 생성한 이미지"
    
    shorten_text_for_image = textwrap.shorten(text_for_image, 200, placeholder=' [..이하 생략..]')
    
    image_urls = my_image_gen.generate_image_from_text(text_for_image, image_num, image_size)

    images = []
    download_file_names = []
    for k, image_url in enumerate(image_urls):
        
        r = requests.get(image_url)
        image_data = r.content
        images.append(image_data)
        
        now_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        download_file_name = f"gen_image_{k}_{now_datetime}.png"
        download_file_names.append(download_file_name)
        
    st.session_state['image_caption'] = image_caption
    st.session_state['shorten_text_for_image'] = shorten_text_for_image
    st.session_state['image_urls'] = image_urls
    st.session_state['download_file_names'] = download_file_names
    st.session_state['images'] = images

st.title("이미지 생성을 위한 설정 ")

input_text = st.text_input("이미지 생성을 위한 설명을 입력하세요.",
                                    "빌딩이 보이는 호수가 있는 도시의 공원")

radio_selected_lang = st.radio('입력한 언어', ['한국어', '영어'],
                                       index=0, horizontal=True)

image_num_options = [1, 2, 3]
image_num = st.radio('생성할 이미지 개수를 선택하세요.',
                      image_num_options, index=0, horizontal=True)

image_size_options = ['256x256', '512x512', '1024x1024']
image_size = st.radio('생성할 이미지 크기를 선택하세요.',
                      image_size_options, index=1, horizontal=True)

detail_description = st.radio('상세 묘사를 추가하겠습니까?',
                      ['Yes', 'No'], index=1, horizontal=True)

clicked = st.button('이미지 생성', on_click=button_callback)

st.title("인공지능 이미지 생성기")

if clicked or st.session_state['download_buttons'] == True:
    display_results()

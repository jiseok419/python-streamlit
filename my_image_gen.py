
import textwrap
from openai import OpenAI

client = OpenAI(
    api_key = "sk-proj-juzXqETQ6LI92zopNEA4T3BlbkFJEU8QkwxHC2oSoDrfBZ4l"
)

def translate_text_for_image(text):    
    user_content = f"Translate the following Korean sentences into English.\n {text}"
    messages = [ {"role": "user", "content": user_content} ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        temperature=0.3,
        n=1
    )

    assistant_reply = response.choices[0].message.content
    
    return assistant_reply # 응답 반환

# OpenAI Chat Completions API를 이용해 이미지를 위한 상세 묘사를 생성하는 함수
def generate_text_for_image(text):

    # 대화 메시지 정의
    user_content = f"Describe the following in 1000 characters to create an image.\n {text}"
    
    messages = [ {"role": "user", "content": user_content} ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages, 
        max_tokens=1000, 
        temperature=0.8,  
        n=1
    )
    
    assistant_reply = response.choices[0].message.content

    return assistant_reply # 응답 반환

def generate_image_from_text(text_for_image, image_num=1, image_size="512x512"):    
    
    shorten_text_for_image = textwrap.shorten(text_for_image, 1000) # 1,000자로 제한
    
    response = client.images.generate(prompt=shorten_text_for_image, n=image_num, size=image_size)
    
    image_urls = [] # 이미지 URL 리스트
    for data in response.data:
        image_url = data.url # 이미지 URL 추출
        image_urls.append(image_url)   
        
    return image_urls # 이미지 URL 리스트 반환


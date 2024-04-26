
import textwrap

import streamlit as st
from PyPDF2 import PdfReader

import my_text_sum

st.set_page_config(page_title="pdf_summary_app", page_icon="📈")

def summarize_PDF_file(pdf_file, lang, trans_checked):
    if pdf_file is not None:
        st.write("PDF 문서를 요약 중입니다. 잠시만 기다려 주세요.")
        reader = PdfReader(pdf_file) 

        text_summaries = []

        for page in reader.pages:
            page_text = page.extract_text()  # 페이지의 텍스트 추출
            text_summary = my_text_sum.summarize_text(page_text, lang)
            text_summaries.append(text_summary)

        token_num, final_summary = my_text_sum.summarize_text_final(text_summaries, lang)

        if final_summary != "":
            shorten_final_summary = textwrap.shorten(final_summary,
                                                     250,
                                                     placeholder=' [..이하 생략..]')

            st.write("- 최종 요약(축약):", shorten_final_summary)

            if trans_checked:
                trans_result = my_text_sum.traslate_english_to_korean_using_openAI(final_summary)
                shorten_trans_result = textwrap.shorten(trans_result,
                                                        200,
                                                        placeholder=' [..이하 생략..]')
                st.write("- 한국어 요약(축약):", shorten_trans_result)
        else:
            st.write("- 통합한 요약문의 토큰 수가 커서 요약할 수 없습니다.")

st.title("PDF 문서를 요약하는 웹 앱")

uploaded_file = st.file_uploader("PDF 파일을 업로드하세요.", type='pdf')

radio_selected_lang = st.radio('PDF 문서 언어', ['한국어', '영어'], index=1, horizontal=True)

if radio_selected_lang == '영어':
    lang_code = 'en'
    checked = st.checkbox('한국어 번역 추가')
else:
    lang_code = 'ko'
    checked = False

clicked = st.button('PDF 문서 요약')

if clicked:
    summarize_PDF_file(uploaded_file, lang_code, checked)

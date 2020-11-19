import streamlit as st
import nltk
import en_core_web_sm
nltk.download('punkt')
#NLP
import spacy
nlp = spacy.load('en_core_web_sm')
from spacy import displacy
HTML_WRAPPER = """<div style="overflow-x: auto; border:1px solid #e6e9ef; border-radius: 0.95rem; padding:1 rem">{}</div>"""

# Summary Pkgs
from gensim.summarization import summarize

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# Function for Sumy Summarization
def sumy_summarizer(docx):
    parser = PlaintextParser.from_string(docx, Tokenizer('english'))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document, 3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result
#NLP
#@st.cache(allow_output_mutation=True)
#@st.cache
def analyze_text(text):
    return nlp(text)

#Web Scraping Pkgs
from bs4 import BeautifulSoup
from urllib.request import urlopen

@st.cache
def get_text(raw_url):
    page = urlopen(raw_url)
    soup = BeautifulSoup(page)
    # create a list comprehension of all the p tags found on the page after inspecting element, then join them
    fetched_text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
    return fetched_text

def main():
    """ Summary and entity checker"""

    st.title('Summary and Entity Checker')

    activities = [ 'Summarize', 'NER Checker', 'NER for URL']
    choice = st.sidebar.selectbox('Select Activity', activities)

    if choice == 'Summarize':
        st.subheader('Summary with NLP')
        raw_text = st.text_area('Enter Text Here', 'Type Here')
        summary_choice = st.selectbox('Summary Choice', ['Gensim', 'Sumy Lex Rank'])

        if st.button('Summarize'):
            if summary_choice == 'Gensim':
                summary_result = summarize(raw_text)

            elif summary_choice == 'Sumy Lex Rank':
                summary_result = sumy_summarizer(raw_text)
            st.write(raw_text)

    if choice == 'NER Checker':
        st.subheader('Named Entity Recognition with SpaCy')
        raw_text = st.text_area('Enter Text Here', 'Type Here')

        if st.button('Analyze'):
            #NLP
            docx = analyze_text(raw_text)
            html = displacy.render(docx, style='ent')
            html = html.replace('\n\n', '\n')
            st.write(html, unsafe_allow_html=True)
            #st.markdown(html, unsafe_allow_html=True)

    if choice == 'NER for URL':
        st.subheader('Analyze ')
        raw_url = st.text_input('Enter URL', 'Type here')
        text_length = st.slider('Length to Preview', 50, 1500)
        if st.button('Extract'):
            if raw_url != 'Type here':
                result = get_text(raw_url)
                len_of_full_text = len(result)
                len_of_short_text = round(len(result)/text_length)
                st.info("Length of full text: {}" .format(len_of_full_text))
                st.info("Length of short text: {}" .format(len_of_short_text))
                st.write(result[:len_of_short_text])
                summary_docx = sumy_summarizer(result)
                docx = analyze_text(summary_docx)
                html = displacy.render(docx, style='ent')
                html = html.replace('\n\n', '\n')
                st.write(html, unsafe_allow_html=True)
                # st.markdown(html, unsafe_allow_html=True)



if __name__=='__main__':
    main()
import os
import re
import time

import requests
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate


# ask for nougat service
def nougat_api(file, api):
    url = api + '/predict/'
    files = {'file': file}
    headers = {'accept': 'application/json'}
    response = requests.post(url, files=files, headers=headers)
    return response


# markdown split return list of content
def get_list(markdown, api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    sections = []
    pattern = re.compile(r'^(#+)\s+(.*)$', re.MULTILINE)
    matches = list(pattern.finditer(markdown))
    for index, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        sections.append("-" * level + f" {title}")
    put_text = "\n".join(sections)
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    title_prompt = PromptTemplate(
        input_variables=["txt"],
        template=""" Help me format the table of contents, and be careful to replace all in-line formulas with $ wrapped form, without displaying the title!only return markdown code！
            {txt} 
            """
    )
    chain = LLMChain(llm=llm, prompt=title_prompt)
    return chain.run(put_text)


# markdown split by big sections
def split_markdown(markdown):
    sections = []
    pattern = re.compile(r'^(#+)\s+(.*)$', re.MULTILINE)
    matches = list(pattern.finditer(markdown))
    last_position = len(markdown)
    for index, match in enumerate(matches):
        level = len(match.group(1))
        title = match.group(2).strip()
        start_position = match.start()
        if index + 1 < len(matches):
            end_position = matches[index + 1].start()
        else:
            end_position = last_position
        section_text = markdown[start_position:end_position].strip()
        sections.append((title, level, section_text))
    return sections


def remove_last_100_chars(text):
    if len(text) > 100:
        return text[:-100]
    else:
        return text


def paper_analysis(api, text):
    os.environ["OPENAI_API_KEY"] = api
    llm = ChatOpenAI(model_name="gpt-3.5-turbo-16k-0613", temperature=0)
    prompt = PromptTemplate(
        input_variables=["txt"],
        template="""
        Use the following step-by-step instructions to respond to user inputs.
        Step 1 - The user will provide you with a complete scientific article in Markdown form. 
                Find the title of it in the very beginning part ,and start your answer also in Markdown form 
                with a prefixed format 
                ""#### Title :""
                newline ""insert title here""
                
        Step 2 - Read the article carefully, and find out why the author write this article, that is, the aim
                of it. Continue your answer in Markdown form with a prefix 
                ""#### Aim :""
                newline ""insert text here (50 words)""
        
        Step 3 - Read the article carefully, and find out how the author achieved the aim, that is, the study method used.
                Continue your answer in Markdown form with a prefix 
                ""#### Method :""
                newline ""insert text here( organized 100 words)""
        Step 4 - Find the main formulas used and list them with a prefixed format 
                ""#### Main formulas: "" 
                newline ""$$latax formula 1$$: One sentence describe why author use it""
                newline ""$$latax formula 2$$: One sentence describe why author use it""
                newline ""$$latax formula 3$$: One sentence describe why author use it""
                ...
        
        {txt}
    """
    )
    chain = LLMChain(llm=llm, prompt=prompt)
    query_result = ""
    try:
        query_result = chain.run(text)
    except Exception as e:
        print(f"Error occurred: {e}")
        text = text[:60000]
        query_result = chain.run(text)

    if query_result == "":
        query_result = "Please give me correct files of article!"
    return query_result


def paper_compare(api, text1, text2):
    os.environ["OPENAI_API_KEY"] = api
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)  # "gpt-3.5-turbo-16k-0613"
    prompt = PromptTemplate(
        input_variables=["txt"],
        template="""
        Use the following step-by-step instructions to respond to user inputs. 
        Step 1 - The user will provide you with a pair of summaries of articles (delimited with XML tags). 
        From their titles compare the topic they talk about, identifying overlapping contributions. 
        Describe similarity degree words [ "No",    "Little",    "Minor",
            "Some",    "Moderate",    "Substantial",    "Considerable",
            "High",    "Strong",    "Very high",    "Nearly identical",
           "Almost identical",    "Identical"]
        Then start your answer also in Markdown form with a prefix format 
        ""#### Topics :[one similarity degree word chosen]"" 
        newline ""insert text here(30 words)"".
                
        Step 2 - Compare the aims of the two articles, identifying overlapping contributions. Then start your answer 
        also in Markdown form with a prefix format 
        ""#### Aims :[one similarity degree word chosen]"" 
        newline ""insert text here(50 words)"".
        
        Step 3 - Compare the Methods of the two articles, identifying overlapping contributions. Then start your 
        answer also in Markdown form with a prefix format 
        ""#### Methods :[one similarity degree word chosen]"" 
        newline ""insert text here(50 words)"". 
        
        Step 4 - Compare the formulas of the two articles, identifying similar formulas pair.
        A pair of similar formulas means that these two formulas are presented separately in two articles, 
        and similar to each other. For example, some formulas that just change the letter symbols but achieve the same 
        function. 
        Then start your answer also in Markdown form with a prefix format 
        ""#### Main formulas :[one similarity degree word chosen]"" 
        If there are any similar formulas, list them in the following format:
                newline ""##### Pair 1: "" 
                newline ""###### $$latax formula 1$$ (in article A): One sentence describe function of it""
                newline ""###### $$latax formula 2$$ (in article B): One sentence describe function of it""
                newline ""###### Similarity: insert text here (30 words)""
                ...
        If formulas resemblance is no, explain it(30 words).
        {txt}
    """
    )
    text = f"""
        <articleA> {text1} </articleA>
        
        <articleB> {text2} </articleB>
    """

    chain = LLMChain(llm=llm, prompt=prompt)
    query_result = chain.run(text)
    return query_result


def paper_compare3(api, analysis1, compare12, compare13):
    os.environ["OPENAI_API_KEY"] = api
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)  # "gpt-3.5-turbo-16k-0613"
    prompt = PromptTemplate(
        input_variables=["txt"],
        template="""
        Use the following step-by-step instructions to respond to user inputs. 
        Step 1 - The user will provide you with 1 summaries of article A and Comparing result between A and B/C(delimited with XML tags). 
        Identify that B and C who are more similar to A?
        Then start your answer also in Markdown form with a prefix format 
        ""#### Topics :B or C (who are more similar to A on topics)"" 
        newline ""insert text here(30 words)"".

        Step 2 - Compare the aims similarity. Then start your answer 
        also in Markdown form with a prefix format 
        ""#### Aims :B or C (who are more similar to A on aims)"" 
        newline ""insert text here(50 words)"".

        Step 3 - 
        ""#### Methods :B or C (who are more similar to A on aims)"" 
        newline ""insert text here(50 words)"". 

        Step 4 - 
        ""#### Main formulas :B or C (who are more similar to A  on topics)"" 
        newline ""insert text here(50 words)"". 
        {txt}
    """
    )
    text = f"""
        <articleA> {analysis1} </articleA>

        <Compare result between A and B> {compare12} </Compare result between A and B>
        
        <Compare result between A and C> {compare13} </Compare result between A and C>
    """

    chain = LLMChain(llm=llm, prompt=prompt)
    query_result = chain.run(text)
    return query_result


if __name__ == "__main__":
    pass

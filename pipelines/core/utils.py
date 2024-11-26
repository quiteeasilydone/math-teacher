from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from wolframclient.evaluation import WolframCloudSession, SecuredAuthenticationKey
from wolframclient.language import wlexpr
import yaml
import os

def build_chain(prompt_path, prompt_name, format_type):
    with open(prompt_path, 'r') as f:
        prompt_data = yaml.safe_load(f)
        prompt_data = prompt_data[prompt_name]
    
    model_configure = prompt_data['configure']
    template = prompt_data['template']
    input_variables = prompt_data['input_variables']
    
    llm = ChatOpenAI(model = model_configure['model'],
                     temperature = model_configure['temperature'],
                     max_tokens=model_configure["maximum_length"],
                     top_p=model_configure['top_p'])
    
    prompt = ChatPromptTemplate.from_messages(
        [(message['role'], message['content']) for message in template]
    )
    
    parser = JsonOutputParser(pydantic_object = format_type)
    
    prompt = prompt.partial(format_instructions = parser.get_format_instructions())
    
    chain_map = {"context" : RunnablePassthrough()}
    
    for var in input_variables:
        if var not in chain_map:
            chain_map[var] = RunnablePassthrough()
    
    chain = (
        chain_map
        | prompt
        | llm
        | parser
    )
    
    return chain

def wolfram_code_result(code):
    sak = SecuredAuthenticationKey(
    os.environ.get['CUNSUMER_KEY'],
    os.environ.get['CUNSUMER_SECERET'])
    # 세션 시작
    session = WolframCloudSession(credentials=sak)
    session.start()
    # 울프람 언어 코드 작성
    # 코드를 세션에서 평가
    result = session.evaluate(wlexpr(code))
    
    session.terminate()
    return result
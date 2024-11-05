from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv

def build_chain(prompt_path, prompt_name, format_type):
    load_dotenv()
    
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
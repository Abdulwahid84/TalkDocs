from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def route(llm, memory):
    """
    Route a question to either vectorstore or general memory.
    Uses simple classification instead of structured output to avoid API issues.
    """
    memory_str = "\n".join(memory) if memory else "No conversation history yet"
    
    system_prompt = f"""You are a question routing expert. Analyze the user's question and decide where to find the answer.

Output ONLY one word:
- If the question is about specific documents, uploaded files, or PDFs: say "vectorstore"
- If the question is general knowledge or about the conversation: say "memory"

Rules:
1. Questions starting with "what is", "who is", "tell me about" -> usually vectorstore (about documents)
2. Questions like "do you remember", "what did we discuss" -> memory
3. Questions about specific names/topics in documents -> vectorstore  
4. General knowledge questions -> memory

Conversation history:
{memory_str}"""

    # Use a simple template that doesn't require memory_str in invoke
    route_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{question}"),
        ]
    )
    
    # Chain: prompt -> LLM -> output parser
    chain = route_prompt | llm | StrOutputParser()
    
    # Wrapper to parse the output and return correct format
    class RouteResult:
        def __init__(self, datasource):
            self.datasource = datasource
    
    def parse_route(question_dict):
        result = chain.invoke(question_dict)
        # Clean the result - take first word only
        datasource = result.strip().lower().split()[0] if result else "memory"
        # Ensure it's vectorstore or memory
        if "vectorstore" in datasource or "document" in datasource or "file" in datasource or "pdf" in datasource:
            return RouteResult("vectorstore")
        else:
            return RouteResult("memory")
    
    # Return a callable that works with the graph
    class RoutingChain:
        def __init__(self, chain_fn):
            self.chain_fn = chain_fn
        
        def invoke(self, input_dict):
            return self.chain_fn(input_dict)
    
    return RoutingChain(parse_route)
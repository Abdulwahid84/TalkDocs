from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from pydantic import BaseModel
from typing import TypedDict, List
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import os

from router import route
from ingestion import PDFIngestor


class GraphState(TypedDict):
    question: str
    response: str
    documents: List[str]


class PdfChat:
    def __init__(self, api_key, retriever):
        self.model = ChatGroq(api_key=api_key, model="llama-3.3-70b-versatile", temperature=0)  # free unlimited model
        builder = StateGraph(GraphState)
        builder.add_node("retrieve", self.retrieve_node)
        builder.add_node("boost_question", self.boost_question)
        builder.add_node("structer_document", self.structer_document)
        builder.add_node("generate_with_rag", self.generate_with_doc)
        builder.add_node("generate", self.generate_wo_doc)

        builder.set_entry_point("boost_question")
        builder.add_conditional_edges(
            "boost_question",
            self.decide_retrieve,
            {
                "retrieve": "retrieve",
                "generate": "generate"
            }
        )
        builder.add_edge("retrieve", "structer_document")
        builder.add_edge("structer_document", "generate_with_rag")
        builder.add_edge("generate_with_rag", END)
        builder.add_edge("generate", END)

        self.retriever = retriever

        self.graph = builder.compile()

        self.memory_list = []  # Simple memory replacement

    def decide_retrieve(self, state: GraphState):
        question = state["question"]
        try:
            source = route(self.model, self.memory_list).invoke({"question": question})
            if hasattr(source, 'datasource'):
                if source.datasource == "vectorstore":
                    return "retrieve"
            else:
                # Fallback if source is a string
                if "vectorstore" in str(source).lower():
                    return "retrieve"
            return "generate"
        except Exception as e:
            # If routing fails, default to generate mode
            print(f"[Warning] Routing error (defaulting to generate): {e}")
            return "generate"

    def boost_question(self, state: GraphState):
        question = state["question"]
        try:
            prompt = """You are an assistant in a question-answering tasks.
                        You have to boost the question to help search in vectorstore.
                        Don't make up random names.
                        Return a better structred question for vectorstore search, but don't make it longer
                        \n
                        Question: {question}
                    """
            prompt = ChatPromptTemplate.from_template(prompt)
            chain = prompt | self.model | StrOutputParser()
            question = chain.invoke({"question": question})
            return {"question": question}
        except Exception as e:
            # If boosting fails, return original question
            print(f"[Warning] Question boost error: {e}")
            return {"question": state["question"]}


    def retrieve_node(self, state: GraphState):
        question = state["question"]
        try:
            documents = self.retriever.invoke(question)
            if not documents:
                return {"documents": "No documents found"}
            return {"documents": documents}
        except Exception as e:
            print(f"[Error] Retrieval failed: {e}")
            return {"documents": "Unable to retrieve documents"}

    def structer_document(self, state: GraphState):
        documents = state["documents"]
        question = state["question"]
        
        try:
            # Handle if documents is a string (from error case)
            if isinstance(documents, str):
                return {"documents": documents}
            
            # Extract page content if documents are objects
            try:
                doc_content = [doc.page_content for doc in documents]
            except:
                doc_content = [str(doc) for doc in documents]

            prompt = """You are an expert assistant for question-answering tasks. 
                        You have to restructure the documents for the question. 
                        Keep it short, only knowledge that is relevant to the question.
                        Don't make up random names.
                        Return a better structured document for better understanding.
                        \n
                        Documents: {documents}
                        \n
                        Question: {question}
                    """
            prompt = ChatPromptTemplate.from_template(prompt)
            chain = prompt | self.model | StrOutputParser()

            document = chain.invoke({"question": question, "documents": "\n".join(doc_content)})
            return {"documents": document}
        except Exception as e:
            print(f"[Error] Document structuring failed: {e}")
            return {"documents": str(documents)}

    def generate_with_doc(self, state: GraphState):
        documents = state["documents"]
        question = state["question"]
        
        try:
            prompt = """You are an expert assistant for question-answering tasks. 
                        Use the provided documents as context to extract and answer the question. 
                        If the answer is not in the context, say 'I don't know.' 
                        Keep answer to three sentences maximum.
                        \n
                        Context: {context}
                        \n
                        Question: {question} 
                        \n
                        Answer:
                    """
            prompt = ChatPromptTemplate.from_template(prompt)
            chain = prompt | self.model | StrOutputParser()

            response = chain.invoke({"question": question, "context": str(documents)})
            return {"response": response}
        except Exception as e:
            print(f"[Error] Generate with document failed: {e}")
            return {"response": f"I encountered an error while processing your question. Please try again."}

    def generate_wo_doc(self, state: GraphState):
        question = state["question"]
        try:
            prompt = """You are a helpful assistant. 
                        If you don't know the answer, say 'I don't know'.
                        Keep answer to three sentences maximum. 
                        Question: {question}
                    """
            prompt = ChatPromptTemplate.from_template(prompt)
            chain = prompt | self.model | StrOutputParser()

            response = chain.invoke({"question": question})
            return {"response": response}
        except Exception as e:
            print(f"[Error] Generate without document failed: {e}")
            return {"response": f"I encountered an error while processing your question. Please try again."}
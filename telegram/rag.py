from llama_index.core import SimpleDirectoryReader

from llama_index.core import VectorStoreIndex, StorageContext,load_index_from_storage
from llama_index.core.storage.docstore import SimpleDocumentStore
from llama_index.core.storage.index_store import SimpleIndexStore
from llama_index.core.vector_stores import SimpleVectorStore
from asgiref.sync import async_to_sync
from llama_index.core.indices import MultiModalVectorStoreIndex
from llama_index.core.schema import ImageDocument
from llama_index.llms.gemini import Gemini
from llama_index.core import PromptTemplate
from llama_index.core import Settings
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core.node_parser import (
    SentenceSplitter,
    SemanticSplitterNodeParser,
)
from llama_index.core.extractors import (
    TitleExtractor,
    QuestionsAnsweredExtractor,
)

from pathlib import Path
from django.conf import settings
from llama_parse import LlamaParse
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import TokenTextSplitter

from bot_src.models import *
from bot_src.constants import *

import os
# #from .models import Collection, DataSource



Settings.embed_model = GeminiEmbedding(
        model_name="models/embedding-001", api_key=gemini_key
    )
# # import torch
# from llama_index.llms.openai import OpenAI
from llama_index.core import PromptTemplate
qa_prompt_tmpl_str = """\
Context information is below.
---------------------
{context_str}
---------------------
Given the context information and not prior knowledge, \
Be polite, answer questions based only on c ontext data.\
you are assistant built to help answer questions about th {context_str}.
When asked about the title respond with the value of the first heading in the document
authors names are located on the first page
Query: {query_str}
Answer: \
"""

query_wrapper_prompt = PromptTemplate(qa_prompt_tmpl_str)
parsing_instruction ="""
The heading on the first page of this document is the Title ( add a title tag to it), Most pages do not have a title
List of names on the first page are authors of the research, Most pages do NOT have authors
"""

gemini_model = Gemini(model="models/gemini-pro", api_key=gemini_key)
Settings.llm = gemini_model
# parser = LlamaParse(
#     api_key=llama_parse_key,
#     result_type='markdown',
#     parsing_instruction=parsing_instruction
# ) 



def load_collection(collection_id):


    parser = LlamaParse(
    api_key=llama_parse_key,
    parsing_instruction=parsing_instruction
)
    extractor = {".pdf":parser}
    collection = Collection.objects.get(id=collection_id)

    collection_path = Path(settings.BASE_DIR)/f"collections/{collection.title}/index"

    directory_path = Path(f"{settings.BASE_DIR}/collections/{collection.title}/")

    gemini_model = Gemini(model="models/gemini-pro", api_key=gemini_key)
    extractor = {".pdf":parser}
    Settings.llm = gemini_model

    text_splitter = TokenTextSplitter(
    separator=" ", chunk_size=512, chunk_overlap=128
)
    
    

    title_extractor = TitleExtractor(nodes=5)
    docs = SimpleDirectoryReader(directory_path, file_extractor=extractor).load_data()

    gemini_model = Gemini(model="models/gemini-pro", api_key=gemini_key)
    Settings.llm = gemini_model

    base_splitter = SentenceSplitter(chunk_size=512)
    
    Settings.llm = gemini_model      
    
    index = VectorStoreIndex.from_documents(docs, transformations=[title_extractor,text_splitter])

    index.set_index_id(collection.title)
    index.storage_context.persist(collection_path)

    return index



def load_index(collection_id, query):

    collection = Collection.objects.get(id=collection_id)
    collection_path = Path(settings.BASE_DIR)/f"collections/{collection.title}/index"

    directory_path = Path(f"{settings.BASE_DIR}/collections/{collection.title}/")

    if not collection_path.exists(): 
        index = load_collection(collection_id=collection_id)
        query_engine = index.as_chat_engine(system_prompt=query_wrapper_prompt)
        response = query_engine.chat(query)
        return response.response

    storage_context = StorageContext.from_defaults(persist_dir=collection_path)
    index = load_index_from_storage(storage_context, index_id=collection.title)
    query_engine = index.as_chat_engine(system_prompt=query_wrapper_prompt)

    response = query_engine.chat(query)
    return response.response
    

def check_conversation(query, collection_id=None, bot_id=None, chat_id=None):
    try:
        if not collection_id or not bot_id or not chat_id:
            collection = Collection.objects.get(title ='test')
            result = load_index(query=query, collection_id=collection.id)
            return result

        collection = Collection.objects.get(id=collection_id)
        bot = Bot.objects.get(id=bot_id)
        chat = TelegramGroup.objects.get(group_id=chat_id)

        conversation = Conversation.objects.filter(collection=collection, bot=bot, group=chat)

        if conversation.exists():
            conversation = Conversation.objects.get(collection=collection, bot=bot, group=chat)

            collection = load_index(
                collection_id=conversation.collection.id,
                query=query
            )

            return collection
        else : # use some base collection
            pass
    except Exception as e:
        print(e)

def add_document_to_index(collection_id, document):
    pass

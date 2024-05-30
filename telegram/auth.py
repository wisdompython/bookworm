# import requests
# apikey = '6542354616:AAGbi0-GcndMZW77y1NxIxCVGdITodFu_Ek'
# url = f"https://api.telegram.org/bot{apikey}/getChat"
# #url = f"https://api.telegram.org/bot{apikey}/sendMessage"
# response = requests.get(url)
# # response = requests.post(url, data={
# #     'text':'hi', 'chat_id':6738668801
# # })

# # print(response.json().keys())
# from llama_index.core.extractors import (
#     SummaryExtractor,
#     QuestionsAnsweredExtractor,
#     TitleExtractor,
#     KeywordExtractor,
#     BaseExtractor,
# )
# from llama_index.extractors.entity import EntityExtractor
# from llama_index.core.node_parser import TokenTextSplitter
# from llama_index.core import Settings
# from llama_index.embeddings.gemini import GeminiEmbedding
# from rag import *
# gemini_key = "AIzaSyAwIN2d4UunKuegUkdSWSz_IauYSUjR1no"


# text_splitter = TokenTextSplitter(
#     separator=" ", chunk_size=512, chunk_overlap=128
# )



# Settings.llm = gemini_model
# class CustomExtractor(BaseExtractor):
#     def extract(self, nodes):
#         metadata_list = [
#             {
#                 "custom": (
#                     node.metadata["document_title"]
#                     + "\n"
#                     + node.metadata["excerpt_keywords"]
#                 )
#             }
#             for node in nodes
#         ]

        
#         return metadata_list


# extractors = [
#     TitleExtractor(nodes=3, llm=gemini_model),
#     #QuestionsAnsweredExtractor(questions=3, llm=gemini_model),
    
#     #EntityExtractor(prediction_threshold=0.5, device='cpu',label_entities=False),
#     #SummaryExtractor(summaries=["prev", "self"], llm=gemini_model),
#     #KeywordExtractor(keywords=10, llm=gemini_model),
#     # CustomExtractor()
# ]
# import random

# random.seed(42)
# # comment out to run on all documents
# # 100 documents takes about 5 minutes on CPU
# #docs = SimpleDirectoryReader(input_files=['./docs/business_Art.pdf'], file_extractor=extractor).load_data()
# #documents = random.sample(docs, 1)

# transformations = [text_splitter] + extractors
# pipeline = IngestionPipeline(transformations=transformations)
# docs = SimpleDirectoryReader(input_files=['./docs/business_Art.pdf']).load_data()

# pipeline.run(documents=docs)


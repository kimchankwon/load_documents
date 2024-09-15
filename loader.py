
import sys
argumentList = sys.argv[1:]
if len(argumentList) != 1:
  print("Usage: python3 loader.py path/to/file")
  exit()

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.vectorstores import SupabaseVectorStore
from langchain_openai import OpenAIEmbeddings
from supabase.client import Client, create_client

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

embeddings = OpenAIEmbeddings()

from langchain_community.document_loaders import PyPDFLoader


loader = PyPDFLoader("COMP9517/Course Outline.pdf")
documents = loader.load()

vector_store = SupabaseVectorStore.from_documents(
    documents,
    embeddings,
    client=supabase,
    table_name="documents",
    query_name="match_documents",
    chunk_size=500
)
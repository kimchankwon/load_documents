import sys
import os
from dotenv import load_dotenv
from supabase.client import Client, create_client
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import List

# Argument Handling
argumentList = sys.argv[1:]
if len(argumentList) != 1:
    print('Usage: python3 topic_extractor.py "path/to/file"')
    exit()

path_name = sys.argv[1]

# Load environment variables
load_dotenv()

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# Load the PDF document using PyPDFLoader
loader = PyPDFLoader(path_name)
documents = loader.load()

# Define a prompt template for extracting topics
prompt = PromptTemplate.from_template(
"""
Course Outline:
{course_outline}

- Extract the main academic topics and subject areas from the course outline.
- Focus on the core subject matter, theories, methodologies, and technical concepts related to the course.
- Exclude logistical information such as assignment details, exam dates, or administrative content.
"""
)

# Define a Pydantic model for the desired output structure
class CourseTopics(BaseModel):
    topics: List[str] = Field(description="List of academic topics extracted from the course outline.")


model = ChatOpenAI(model="gpt-4o", temperature=0)
structured_llm = model.with_structured_output(CourseTopics)
# Generate the course outline text from the documents
course_outline_text = "\n\n".join([doc.page_content for doc in documents])

# Invoke the prompt with the course outline and parse the output
formatted_prompt  = prompt.format(course_outline=course_outline_text)
response = structured_llm.invoke(formatted_prompt)

course_code = path_name.split('/')[0]

update_response = (
    supabase.table("courses")
    .update({"topics": response.topics})
    .eq("code", course_code)
    .execute()
)
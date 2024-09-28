from dotenv import load_dotenv
from PyPDF2 import PdfReader
import docx2txt
from langchain_openai import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain import PromptTemplate
import json
import os
 
load_dotenv()
 
api_key = os.getenv('API_KEY')
azure_endpoint = os.getenv('AZURE_ENDPOINT')
openai_api_version = os.getenv('OPENAI_API_VERSION')
deployment_name = os.getenv('DEPLOYMENT_NAME')
 
llm = AzureChatOpenAI(
    openai_api_version=openai_api_version,
    azure_endpoint=azure_endpoint,
    openai_api_key=api_key,
    openai_api_type="azure",
    deployment_name=deployment_name,
    model="gpt-4o"
)

function_descriptions = [
    {
        "name": "scan_resume",
        "description": "Scans a resume and returns relevant information",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the person"
                },
                "email": {
                    "type": "string",
                    "description": "Email of the person"
                },
                "phone": {
                    "type": "string",
                    "description": "Phone number of the person"
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "school": {
                                "type": "string",
                                "description": "Name of the school"
                            },
                            "degree_or_certificate": {
                                "type": "string",
                                "description": "Degree or certificate"
                            },
                            "time_period": {
                                "type": "string",
                                "description": "Time period of education"
                            },
                        },
                    },
                    "description": "Education of the person",
                },
                "employment": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company": {
                                "type": "string",
                                "description": "Name of the company"
                            },
                            "title": {
                                "type": "string",
                                "description": "Title of the person"
                            },
                            "time_period": {
                                "type": "string",
                                "description": "Time period of employment"
                            },
                        },
                    },
                    "description": "Employment history of the person",
                },
                "skills": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "Skills of the person"
                    },
                },
            },
            "required": ["name", "email", "skills"]
        }
    }
]
 
# Function descriptions remain the same
# function_descriptions = [
#     {
#         "name": "scan_resume",
#         "description": "Scans a resume and returns relevant information",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "name": {
#                     "type": "string",
#                     "description": "Name of the person"
#                 },
#                 "email": {
#                     "type": "string",
#                     "description": "Email of the person"
#                 },
#                 "phone": {
#                     "type": "string",
#                     "description": "Phone number of the person"
#                 },
#                 "education": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "properties": {
#                             "school": {
#                                 "type": "string",
#                                 "description": "Name of the school"
#                             },
#                             "degree_or_certificate": {
#                                 "type": "string",
#                                 "description": "Degree or certificate"
#                             },
#                             "time_period": {
#                                 "type": "string",
#                                 "description": "Time period of education"
#                             },
#                         },
#                     },
#                     "description": "Education of the person",
#                 },
#                 "employment": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "properties": {
#                             "company": {
#                                 "type": "string",
#                                 "description": "Name of the company"
#                             },
#                             "title": {
#                                 "type": "string",
#                                 "description": "Title of the person"
#                             },
#                             "time_period": {
#                                 "type": "string",
#                                 "description": "Time period of employment"
#                             },
#                         },
#                     },
#                     "description": "Employment history of the person",
#                 },
#                 "skills": {
#                     "type": "array",
#                     "items": {
#                         "type": "string",
#                         "description": "Skills of the person"
#                     },
#                 },
#             },
#             "required": ["name", "email", "skills"]
#         }
#     }
# ]
 
template = """/
Scan the following resume and return the relevant details.
If the data is missing just return N/A
Resume: {resume}
"""
 
 
def main():
    print("# Resume Scanner")
    file_path = r'Vienna-Modern-Resume-Template.pdf'
 
    text = ""
    try:
        if file_path.endswith(".pdf"):
            with open(file_path, "rb") as file:
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
 
        elif file_path.endswith(".docx"):
            text += docx2txt.process(file_path)
        else:
            print("Unsupported file format. Please use PDF or DOCX.")
            return
 
    except Exception as e:
        print(f"Error reading the file: {e}")
        return
 
    prompt = PromptTemplate.from_template(template)
    content = prompt.format(resume=text)
 
    try:
        response = llm.invoke(
            input=content,
            functions=function_descriptions
        )
 
        function_call = response.additional_kwargs['function_call']
        data = json.loads(function_call['arguments'])
 
        # Print extracted information
        print("\n## Resume Details ##")
        print(f"Name: {data['name']}")
        print(f"Email: {data['email']}")
        print(f"Phone: {data.get('phone', 'N/A')}")
       
        print("\nEducation:")
        for education in data.get('education', []):
            print(f" - School: {education.get('school', 'N/A')}")
            print(f"   Degree/Certificate: {education.get('degree_or_certificate', 'N/A')}")
            print(f"   Time Period: {education.get('time_period', 'N/A')}")
       
        print("\nEmployment History:")
        for employment in data.get('employment', []):
            print(f" - Company: {employment.get('company', 'N/A')}")
            print(f"   Title: {employment.get('title', 'N/A')}")
            print(f"   Time Period: {employment.get('time_period', 'N/A')}")
       
        print("\nSkills:")
        for skill in data.get('skills', []):
            print(f" - {skill}")
 
    except Exception as e:
        print(f"Error processing the resume: {e}")
 
 
if __name__ == '__main__':
    main()
 
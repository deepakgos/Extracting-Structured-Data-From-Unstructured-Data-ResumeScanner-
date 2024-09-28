# Resume Scanner

This Python script processes resumes in PDF or DOCX formats and extracts relevant details such as name, email, phone number, education, employment history, and skills using the Azure OpenAI API.

## Features

- Extract text from resume files (`.pdf` or `.docx`)
- Send resume data to an Azure OpenAI-powered language model to scan and extract information
- Retrieve structured resume details including:
  - Name
  - Email
  - Phone number (if available)
  - Education (school, degree, time period)
  - Employment history (company, title, time period)
  - Skills

## Prerequisites

Ensure you have the following set up before running the script:

1. **Python 3.8+**
2. **Required Libraries:** Install the required libraries using pip:
    ```bash
    pip install -r requirements.txt
    ```
    Contents of `requirements.txt`:
    ```
    python-dotenv
    PyPDF2
    docx2txt
    langchain-openai
    ```

3. **Environment Variables:**
    Create a `.env` file in the root of your project with the following variables:
    ```bash
    API_KEY=<your_openai_api_key>
    AZURE_ENDPOINT=<your_azure_endpoint>
    OPENAI_API_VERSION=<your_openai_api_version>
    DEPLOYMENT_NAME=<your_openai_deployment_name>
    ```

## How to Use

1. **Place Resume Files**: Add a `.pdf` or `.docx` resume to be processed. Update the `file_path` variable in the `main()` function with the path to your resume file.

2. **Run the Script**: Execute the script:
    ```bash
    python resume_scanner.py
    ```

3. **View the Results**: The extracted details from the resume will be printed to the console.

## Example Output

After running the script, the output will look like this:

# Resume Scanner

## Resume Details ##

Name: John Doe  
Email: johndoe@example.com  
Phone: 123-456-7890

Education:
 - School: ABC University  
   Degree/Certificate: Bachelor's in Computer Science  
   Time Period: 2016-2020

Employment History:
 - Company: XYZ Corp  
   Title: Software Engineer  
   Time Period: 2020-2023

Skills:
 - Python
 - Machine Learning
 - Data Analysis


## Error Handling

If the script encounters an error while reading the file or processing the data, an error message will be displayed in the console.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

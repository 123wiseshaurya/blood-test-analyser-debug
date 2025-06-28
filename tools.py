## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from crewai.tools.base_tool import Tool

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7,
    api_key=os.getenv("OPENAI_API_KEY")
)

## Creating search tool
# Note: SerperDevTool removed as it's not essential for basic functionality
search_tool = None

## Creating custom pdf reader tool
def read_data_tool(file_path='data/sample.pdf'):
    """Tool to read data from a pdf file from a path

    Args:
        file_path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full Blood Test report file
    """
    
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            return f"Error: File not found at path {file_path}"
        
        # Check if file is readable
        if not os.access(file_path, os.R_OK):
            return f"Error: File at {file_path} is not readable"
        
        # Load and parse PDF
        docs = PyPDFLoader(file_path=file_path).load()
        
        if not docs:
            return f"Error: No content found in PDF file {file_path}"

        full_report = ""
        for i, data in enumerate(docs):
            # Clean and format the report data
            content = data.page_content
            
            # Remove extra whitespaces and format properly
            while "\n\n" in content:
                content = content.replace("\n\n", "\n")
                
            full_report += f"Page {i+1}:\n{content}\n\n"
            
        if not full_report.strip():
            return f"Error: No readable text content found in PDF file {file_path}"
            
        return full_report
        
    except Exception as e:
        return f"Error reading PDF file {file_path}: {str(e)}"

# Create CrewAI Tool
blood_test_tool = Tool(
    name="Blood Test Report Reader",
    description="Read and extract text content from blood test report PDF files",
    func=read_data_tool
)

## Creating Nutrition Analysis Tool
class NutritionTool:
    async def analyze_nutrition_tool(blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool:
    async def create_exercise_plan_tool(blood_report_data):        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"
import streamlit as st
import cohere
import subprocess
import tempfile

# Initialize the Cohere client with your API key
api_key = 'DWYlDQorZ6fUuT2Hfzh02vlWdWML0l6jXLuUhFVX'
co = cohere.Client(api_key)

def generate_documentation(code, language):
    """Generate documentation for the given code using Cohere's API."""
    prompt = f"""
    Analyze the following {language} code and generate concise documentation that includes:
    - Descriptions of classes and their attributes
    - Descriptions of functions, including parameters and return values
    - Usage examples where applicable

    Code:
    {code}
    
    Documentation:
    """
    
    try:
        response = co.generate(
            model='command-xlarge-nightly',
            prompt=prompt,
            max_tokens=500,
            temperature=0.3,
        )
        # Return the generated text
        return response.generations[0].text.strip()
    except Exception as e:
        return f"An error occurred during documentation generation: {str(e)}"

def analyze_code_with_pylint(code):
    """Analyze Python code with pylint and return the output."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode())
        temp_file.close()
        
        try:
            results = subprocess.run(
                ['pylint', temp_file.name],
                capture_output=True,
                text=True
            )
            return results.stdout
        except Exception as e:
            return f"An error occurred during pylint analysis: {str(e)}"

def analyze_code_with_eslint(code):
    """Analyze JavaScript code with eslint and return the output."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".js") as temp_file:
        temp_file.write(code.encode())
        temp_file.close()

        try:
            results = subprocess.run(
                ['eslint', temp_file.name],
                capture_output=True,
                text=True
            )
            return results.stdout
        except Exception as e:
            return f"An error occurred during eslint analysis: {str(e)}"

# Streamlit interface
st.title('Automated Code Documentation and Debugging Tool ')

# Language selection
languages = [
    "Python", "JavaScript", "Java", "C++", "Ruby", "Go", "C#", "Swift", "Kotlin", "PHP",
    "TypeScript", "Rust", "Scala", "Haskell", "Perl", "Lua", "Shell", "R", "MATLAB", "HTML",
    "CSS", "SQL", "Dart", "Objective-C"
]

# Define file types for each language
file_types = {
    "Python": "py",
    "JavaScript": "js",
    "Java": "java",
    "C++": "cpp",
    "Ruby": "rb",
    "Go": "go",
    "C#": "cs",
    "Swift": "swift",
    "Kotlin": "kt",
    "PHP": "php",
    "TypeScript": "ts",
    "Rust": "rs",
    "Scala": "scala",
    "Haskell": "hs",
    "Perl": "pl",
    "Lua": "lua",
    "Shell": "sh",
    "R": "r",
    "MATLAB": "m",
    "HTML": "html",
    "CSS": "css",
    "SQL": "sql",
    "Dart": "dart",
    "Objective-C": "m"
}

language = st.selectbox("Choose a programming language", languages)
file_extension = file_types.get(language)

# File uploader
uploaded_file = st.file_uploader(f"Choose a {language} file", type=file_extension)

if uploaded_file is not None:
    code = uploaded_file.read().decode("utf-8")
    
    # Generate documentation
    documentation = generate_documentation(code, language)
    st.subheader("Generated Documentation")
    st.write(documentation)

    # Debug code with a debugger
    if language == "Python":
        st.subheader("Python Code Analysis")
        pylint_output = analyze_code_with_pylint(code)
        st.text_area("Pylint Output", pylint_output, height=300)
    elif language == "JavaScript":
        st.subheader("JavaScript Code Analysis")
        eslint_output = analyze_code_with_eslint(code)
        st.text_area("ESLint Output", eslint_output, height=300)

    # Add more debuggers for other languages if needed
    # For example, you can add similar functions for Java, C++, etc.

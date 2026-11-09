#  WriteWise AI – Intelligent Writing Assistant

WriteWise AI is an AI-powered writing assistant built using Python and Streamlit. It helps users generate different types of written content using Generative AI models from Google Gemini and OpenAI.

The application provides a simple interface where users can choose a writing task, select a tone, customize content length, and generate content based on their requirements.

##  Features

- **Multiple AI Providers:** Supports Google Gemini and OpenAI.
- **Blog Writing:** Generate informative and engaging blog posts.
- **Email Drafting:** Create professional email drafts.
- **Code Explanation:** Generate easy-to-understand code explanations.
- **Social Media Posts:** Create content for social media.
- **Multiple Writing Styles:** Choose from professional, friendly, formal, creative, academic, and other tones.
- **Custom Content Length:** Generate short, medium, or long content.
- **Target Audience:** Customize content for students, professionals, developers, and more.
- **Creativity Control:** Adjust the AI creativity level.
- **Download Content:** Download generated content in Markdown or text format.

##  Technologies Used

- Python
- Streamlit
- Google Gemini API
- OpenAI API
- Google Gen AI SDK
- OpenAI Python SDK
- Python-dotenv

##  Project Structure

```text
WriteWise-AI/
│
├── app.py
├── requirements.txt
├── .gitignore
└── README.md
```

##  Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/adikulkarni28/WriteWise-AI.git
```

### 2. Open the project folder

```bash
cd WriteWise-AI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

For macOS/Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure API keys

Create a `.env` file in the project directory and add your API keys:

```env
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

Obtain API keys from:

- Google Gemini: https://aistudio.google.com/apikey
- OpenAI: https://platform.openai.com/api-keys

**Important:** Never upload your `.env` file or share your API keys publicly.

### 7. Run the application

```bash
streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

##  How to Use

1. Launch the application.
2. Select Google Gemini or OpenAI as the AI provider.
3. Choose the AI model.
4. Select the type of content you want to generate.
5. Choose the writing tone and content length.
6. Enter your topic or instructions.
7. Click **Generate Content**.
8. View and download the generated content.

##  Future Scope

- Grammar checking and correction.
- AI-powered text rewriting.
- Writing history and saved drafts.
- Additional language support.

## Developer

**Aditya Kulkarni**

GitHub: https://github.com/adikulkarni28

LinkedIn: https://www.linkedin.com/in/aditya-kulkarni-027a862bb/

## License

This project is developed as an academic mini project for learning and educational purposes.
# AI File Sorter

An AI-powered Python tool that automatically organizes files into folders using the OpenAI API.

The program scans a directory, reads a short preview of each file, sends the preview to an AI model for classification, and then moves the file into the appropriate folder.

This project demonstrates practical use of AI APIs for real-world automation tasks.

## Features

- AI-powered file classification
- Automatic folder creation
- Dry-run safety mode (preview before moving files)
- Prevents overwriting existing files
- Error handling for API failures
- Cross-platform file paths (Windows / macOS / Linux)

## How It Works

The program follows this workflow:
Scan the directory given by user -> Read preview of file (first 500 characters) -> Send preview to AI Model -> AI returns category -> Create folder if needed -> Move file into folder

## Installation

Clone the repository:

```
bash
git clone https://github.com/YOUR_USERNAME/ai-file-sorter.git
cd ai-file-sorter
```

Install Dependencies:
pip install -r requirements.txt

Setup API Key (You need one from Open AI):

Windows:
setx OPENAI_API_KEY "your_api_key_here"
For Mac/Linux:
export OPENAI_API_KEY "your_api_key_here"

## What I Learned

1. While building this project, I gained practical experience with several important concepts in software development and AI integration.
2. One of the biggest things I learned was how APIs work in real-world applications. Instead of just learning about APIs in theory, I implemented actual communication between my Python program and the OpenAI API. This helped me understand how requests are sent, how responses are structured, and how to safely manage API keys using environment variables.
3. I also learned how large language models can be used for practical automation tasks. In this project, the AI is used to classify files based on a short preview of their contents. This showed me how prompt design and constraints can influence the output of an AI model and why it is important to guide the model carefully to avoid inconsistent results.
4. Another important lesson was designing software with safety in mind. Since this program moves files around the filesystem, I implemented a dry-run mode so the user can preview what will happen before actually moving any files. This taught me the importance of building safeguards into automation tools.
5. From a programming perspective, this project strengthened my understanding of Python file system operations using modules like `os` and `shutil`. I learned how to safely construct file paths across different operating systems, scan directories, read file previews, and move files programmatically.
6. Finally, I learned how to structure a small project in a clean and readable way by separating the logic into functions, adding clear comments, and documenting the project properly with a README so that others can understand how it works.

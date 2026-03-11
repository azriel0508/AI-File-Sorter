# allows us to interact with our files and filesystem
import os

# shutil gives us higher-level file operations like moving files and creating folders
import shutil

# this is the OpenAI library that lets our Python code communicate with the AI API
from openai import OpenAI

# creating a client object which will handle communication with OpenAI servers
client = OpenAI()

# FUNCTION: Scan a directory and return all file paths

# In this function we read in a directory given by the user,
# then we list everything inside that directory.
# We filter only the files (not folders),
# and return a list containing the full file paths.
def get_files_in_directory(directory):

    files = []

    # os.listdir() returns everything inside the directory:
    # files AND folders
    for item in os.listdir(directory):

        # os.path.join safely builds a file path
        # this is important because Windows uses "\" while Linux/Mac use "/"
        full_path = os.path.join(directory, item)

        # we only want actual files, not folders
        if os.path.isfile(full_path):

            # append the full path of the file to our list
            files.append(full_path)

    # return the list of files we discovered
    return files

# FUNCTION: Read a preview of a file

# This function reads the FIRST part of a file.
# We do this because sending entire files to the AI would:
# 1) cost more tokens (more money)
# 2) be slower
# 3) be unnecessary for classification
def read_file_preview(file_path, char_limit=500):

    try:

        # open the file in read mode
        # encoding utf-8 is standard text encoding
        # errors="ignore" prevents crashes if the file contains weird characters
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

            # read only the first 500 characters
            # this usually contains enough context for classification
            content = file.read(char_limit)

            return content

    except:
        # if anything goes wrong (binary file, unreadable file, etc.)
        # we simply return an empty preview
        return ""

# FUNCTION: Move a file safely into its category folder

def move_file(file_path, category, base_directory, dry_run):

    # build the destination folder path
    destination_folder = os.path.join(base_directory, category)

    # create the folder if it does not already exist
    # exist_ok=True prevents Python from crashing if the folder already exists
    os.makedirs(destination_folder, exist_ok=True)

    # extract just the file name from the full path
    # example:
    # C:\Users\felix\Downloads\file.pdf -> file.pdf
    file_name = os.path.basename(file_path)

    # construct the new path where the file will be moved
    destination_path = os.path.join(destination_folder, file_name)

    # safety check: do not overwrite files
    if os.path.exists(destination_path):
        print(f"Skipping {file_name} because it already exists.")
        return

    # if the user selected dry run mode, we only simulate the move
    if dry_run:
        print(f"[DRY RUN] Would move {file_name} -> {category}")

    else:
        # actually move the file
        shutil.move(file_path, destination_path)
        print(f"Moved {file_name} -> {category}")

# FUNCTION: Ask AI to classify a file

def classify_file(client, instruction, file_name, preview):

    # We construct a PROMPT which will be sent to the AI.
    # A prompt is simply structured text explaining the task.

    # The AI does not see our code.
    # It only sees this text instruction.

    prompt = f"""
Instruction: {instruction}

File name: {file_name}

File preview:
{preview}

Choose ONLY one category from the list below:

School
Work
Personal
Software
Images

Return ONLY the category name exactly as written above.
Do not invent new categories.
Do not explain your answer.
"""
    
    # Here our Python program sends a request to OpenAI's servers.
    # This is an API request over the internet.

    # client.chat.completions.create() sends the prompt to the AI model
    response = client.chat.completions.create(

        # gpt-4o-mini is a fast and cheap model ideal for classification
        model="gpt-4o-mini",

        # messages represent the conversation with the AI
        # role="user" means we are sending an instruction to the AI
        messages=[
            {"role": "user", "content": prompt}
        ],

        # temperature controls randomness
        # temperature=0 means the AI will choose the most probable answer
        # this ensures consistent classification results
        temperature=0
    )

    # EXTRACTING THE AI RESPONSE
    # The API returns a structured JSON response.
    # The actual answer from the AI is inside:

    category = response.choices[0].message.content.strip()

    return category

# MAIN PROGRAM

if __name__ == "__main__":

    # ask the user which folder they want to organize
    directory = input("Enter folder path: ")

    # ask the user how they want the files grouped
    instruction = input("How should the files be organised? ")

    # ask if we should run in dry-run mode
    dry_run_input = input("Run in dry-run mode first? (y/n): ").lower()

    dry_run = dry_run_input == "y"

    # get all files from the directory
    files = get_files_in_directory(directory)

    print("\nAI is cleaning up your files...\n")

    # limit to first 10 files for testing
    for file_path in files[:10]:

        # extract just the file name
        file_name = os.path.basename(file_path)

        # read preview of the file
        preview = read_file_preview(file_path)

        try:

            # send the file information to the AI for classification
            category = classify_file(client, instruction, file_name, preview)

        except Exception as e:

            # if something goes wrong with the API request
            print(f"Error classifying {file_name}: {e}")
            continue

        # show the classification result
        print(f"{file_name} -> {category}")

        # move or simulate moving the file
        move_file(file_path, category, directory, dry_run)
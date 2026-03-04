#allows us to interact with our files
import os 
from openai import OpenAI

client = OpenAI()

#In this function we read in a directory given by the user, 
# then we list everything inside that directory
# we filter only the files in it
# then we return the file paths
def get_files_in_directory(directory):
    files = []

    for item in os.listdir(directory): #going through all the files and items in the directory
        full_path = os.path.join(directory, item)  

        if os.path.isfile(full_path): #checks if its a file then we append its full path in our list
            files.append(full_path)

    #returns a list of files found
    return files

#So we take in the arguments path of the file and the limit of the number of characters we can read
def read_file_preview(file_path, char_limit=500):
    try:
        #Read the file
        with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
            #Read only the first 500 characters in the file so we can classify it base on that
            content = file.read(char_limit)
            return content
    except: #If we get any error we return an empty string
        return ""
    
#Our first talk with AI:
def classify_file(client, instruction, file_name, preview):

    #Creating a efficient prompt for better probability of a accurate answer
    #Preview is the first 500 characters in the file
    #Instruction is given by user
    #File name is the file name we get from the list
    prompt = f"""
Instruction: {instruction}

File name: {file_name}

File preview:
{preview}

Choose ONE category that best fits the file.

Return only the category name.
"""
    response = client.chat.completion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        #temperature = 0 is so that we set the Ai to always give us the highest probable answer
        #Pick the token with the highest probability.
        temperature=0
    )

    return response.choices[0].message.content.strip()

#Main:
if __name__ == "__main__":
    #Ask the user for the folder path that they want
    directory = input("Enter folder path: ")
    instruction = input("How should the files be organised? ")

    #Use our function to get all files
    files = get_files_in_directory(directory)

    #Prints out all the files found
    print("\nfel cleaning up your files....\n")

    for file_path in files:
        #to get the name ONLY of the file
        file_name = os.path.basename(file_path)
        #Use our function to see whats inside the file (First 500 characters)
        preview = read_file_preview(file_path)
        #Classify the file with AI using our python function
        category = classify_file(client, instruction, file_name, preview)

        print(f"{file_name} -> {category}")
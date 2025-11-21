import os

KB_FOLDER = r"C:\Users\sneha\alz-chatbot\kb\en"

kb_data = {}

# Loop through all files once
for file_name in os.listdir(KB_FOLDER):
    file_path = os.path.join(KB_FOLDER, file_name)
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        kb_data[file_name] = content  # store content
        print(f"Content of {file_name}:\n{content}\n---\n")  # also print

# Now kb_data has all your KB files mapped by filename
print("All KB files loaded:", list(kb_data.keys()))

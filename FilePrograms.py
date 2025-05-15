from collections import defaultdict

# Define the directory structure and selected files
files = [
    "/a/a.txt",
    "/a/b/a.txt",
    "/a/b/b.txt",
    "/a/c/z.txt",
    "/a/c/k.txt"
]

# Selected files
selected_files = {
    "/a/a.txt",
    "/a/b/a.txt",
    "/a/b/b.txt"
}

# Step 1: Organize the files by directories
directories = defaultdict(list)

for file in files:
    directories["/".join(file.split("/")[:-1])].append(file)

# Step 2: Consolidate directories where all files are selected
output = []

for directory, all_files in directories.items():
    selected_in_directory = [file for file in all_files if file in selected_files]
    
    if len(selected_in_directory) == len(all_files):
        # If all files are selected, output the directory itself
        output.append(f"-{directory}")
    else:
        # If not all files are selected, output individual files
        for file in selected_in_directory:
            output.append(f"-{file}")

# Output the minimized list
for line in output:
    print(line)

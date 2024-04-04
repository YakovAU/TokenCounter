import tkinter as tk
from tkinter import filedialog
import os
import fnmatch


def is_text_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            f.read(1024)  # Try reading a small portion to check if it's text
    except UnicodeDecodeError:
        return False
    except Exception as e:
        print(f"Error reading file (might be binary or corrupted): {file_path}, {e}")
        return False
    return True


def count_tokens_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            tokens = content.split()
            return len(tokens)
    except Exception as e:
        print(f"Error reading file: {file_path}, {e}")
        return 0


def count_tokens_in_directory(directory, patterns):
    total_tokens = 0
    for root, dirs, files in os.walk(directory):
        filtered_files = []
        for pattern in patterns:
            filtered_files.extend(fnmatch.filter(files, pattern))
        for file in set(filtered_files):  # Remove duplicates
            file_path = os.path.join(root, file)
            if is_text_file(file_path):
                print(f"Reading file: {file_path}")
                total_tokens += count_tokens_in_file(file_path)
    return total_tokens


def count_tokens_in_files(files):
    total_tokens = 0
    for file in files:
        if is_text_file(file):
            print(f"Reading file: {file}")
            total_tokens += count_tokens_in_file(file)
    return total_tokens


def main():
    choice = input("Token Counter\n1 - Files\n2 - Folders\n3 - Specify Pattern(s)\nSelect option (1, 2, or 3): ")

    root = tk.Tk()
    root.withdraw()  # Hide the main window

    if choice == '1':
        file_paths = filedialog.askopenfilenames(title="Select files")  # This should return a tuple
        file_paths = root.tk.splitlist(file_paths)  # Convert tuple to a list of paths
        if file_paths:
            print("Selected files:")
            for file in file_paths:
                print(file)
            total_tokens = count_tokens_in_files(file_paths)
            print(f"\nTotal tokens in selected files: {total_tokens}")
        else:
            print("No files selected.")
    elif choice == '2':
        directory_path = filedialog.askdirectory(title="Select folder")
        if directory_path:
            print(f"Reading files in directory: {directory_path}")
            total_tokens = count_tokens_in_directory(directory_path, ['*'])
            print(f"\nTotal tokens in selected folder: {total_tokens}")
        else:
            print("No folder selected.")
    elif choice == '3':
        directory_path = filedialog.askdirectory(title="Select folder")
        if directory_path:
            pattern_input = input("Enter file patterns separated by spaces (e.g., *.cpp *.h): ")
            patterns = pattern_input.split()
            print(f"Reading files in directory: {directory_path} with patterns: {patterns}")
            total_tokens = count_tokens_in_directory(directory_path, patterns)
            print(f"\nTotal tokens in selected folder with patterns {patterns}: {total_tokens}")
        else:
            print("No folder selected.")
    else:
        print("Invalid option.")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()

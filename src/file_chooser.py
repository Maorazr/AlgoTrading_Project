import os

def choose_file(directory=None):
    files = list_files_in_directory(directory)

    print("Select a file by entering its number:")

    for index, file_name in enumerate(files, start=1):
        print(f"{index}: {file_name}")

    while True:
        try:
            user_choice = int(input("Enter the number of the desired file: "))
            if 1 <= user_choice <= len(files):
                chosen_file = files[user_choice - 1]
                print(f"You have chosen: {chosen_file}")
                return chosen_file
            else:
                print("Invalid number. Please choose a number from the list.")
        except ValueError:
            print("Please enter a valid number.")

def list_files_in_directory(directory=None):
    if directory is None:
        directory = os.getcwd()
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return files

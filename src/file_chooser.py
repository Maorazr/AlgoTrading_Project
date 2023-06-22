import os
import pandas as pd


def choose_file_with_back_option(data_directory):
    while True:
        file_list = os.listdir(data_directory)
        valid_files = [f for f in file_list if f.endswith('.csv')]

        print("Select a file by entering its numsliber:")
        for i, file in enumerate(valid_files, 1):
            print(f"{i}: {file}")

        chosen_file_number = input(
            "Enter the number of the desired file (or type 'back' to go back): ")

        if chosen_file_number.lower() == 'back':
            return None

        try:
            chosen_file_number = int(chosen_file_number)
            if 1 <= chosen_file_number <= len(valid_files):
                return valid_files[chosen_file_number - 1]
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")


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
    files = [f for f in os.listdir(directory) if os.path.isfile(
        os.path.join(directory, f))]
    return files


def load_data_from_directory(default_directory=None):
    while True:
        data_directory = input(
            "Enter the path of the directory containing data files or press enter for default: ")

        if data_directory.lower() == 'back':
            return None
        elif data_directory.strip() == '':
            data_directory = default_directory

        if not os.path.isdir(data_directory):
            print("The provided directory does not exist. Please try again.")
        else:
            chosen_file = choose_file_with_back_option(data_directory)

            if chosen_file is None:
                continue

            input_name, _ = os.path.splitext(chosen_file)
            etf_data = pd.read_csv(os.path.join(
                data_directory, f"{input_name}.csv"))
            return etf_data  # Return the loaded DataFrame


def validated_input(prompt, validation_fn, *args):
    while True:
        try:
            value = input(prompt)
            return validation_fn(value, *args)
        except Exception as e:
            print(f"Invalid input, please try again. Error: {e}")


def parse_ticker_list(input_str, etf_list):
    if input_str.strip() == '':
        return etf_list
    else:
        tickers = [ticker.strip().upper() for ticker in input_str.split(',')]
        tickers.extend(etf_list)
        return tickers


def parse_date_range(value):
    start_date, end_date = value.split(',')
    return start_date.strip(), end_date.strip()


def parse_int_list(value, default=None):
    if value.strip() == '':
        value = default
    return [int(w.strip()) for w in value.split(',')]


def parse_cci_params(value, default=None):
    if value.strip() == '':
        value = default
    cci_period, cci_std = map(float, value.split(','))
    return [int(cci_period), cci_std]


def parse_rsi_window(value, default=None):
    if value.strip() == '':
        value = default
    return int(value.strip())


def validate_float_input(value, default=None, min_value=None, max_value=None):
    if value.strip() == '':
        if default is not None:
            return default
        else:
            raise ValueError("Input cannot be empty.")

    float_value = float(value)

    if min_value is not None and float_value < min_value:
        raise ValueError(
            f"Value should be greater than or equal to {min_value}.")

    if max_value is not None and float_value > max_value:
        raise ValueError(f"Value should be less than or equal to {max_value}.")

    return float_value


def validate_string_input(value, allowed_values=None):
    value = value.strip()

    if not value:
        raise ValueError("Input cannot be empty.")

    if allowed_values is not None and value not in allowed_values:
        raise ValueError(
            f"Value should be one of the following: {', '.join(allowed_values)}")

    return value

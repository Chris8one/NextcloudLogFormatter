import json
import sys
import os
from datetime import datetime

def get_available_filename(base_filename):
    # Function to generate an available filename with incremental numbering
    if not os.path.exists(base_filename):
        return base_filename

    # If the file already exists, increment the number until an available filename is found
    index = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}_{index}.txt"
        if not os.path.exists(new_filename):
            return new_filename
        index += 1

def format_log_entry(log_entry):
    level_mapping = {
        0: "DEBUG",
        1: "INFO",
        2: "WARNING",
        3: "ERROR",
        4: "FATAL"
    }

    try:
        log_json = json.loads(log_entry)
        log_level = log_json.get("level", -1)

        # Map the log level to text representation
        log_level_text = level_mapping.get(log_level, "UNKNOWN")

        formatted_log = f"{log_level_text}\n"
        formatted_log += f"Time: {log_json.get('time')}\n"
        formatted_log += f"User: {log_json.get('user')}\n"
        formatted_log += f"Method: {log_json.get('method')}\n"
        formatted_log += f"URL: {log_json.get('url')}\n"
        formatted_log += f"Message: {log_json.get('message')}\n"

        return formatted_log

    except json.JSONDecodeError as e:
        # Print an error message if JSON decoding fails
        print(f"Error decoding JSON: {e}")
        return None

def format_and_analyze_logs(input_file, filtered_output_file, all_output_file):
    with open(input_file, 'r') as f:
        log_content = f.read().splitlines()

    # Format the log file with a level filter for levels 3 and 4
    filtered_logs = [format_log_entry(log_entry) for log_entry in log_content if format_log_entry(log_entry) is not None and json.loads(log_entry).get("level", -1) in [3, 4]]

    # Format the entire log file without a level filter
    all_logs = [format_log_entry(log_entry) for log_entry in log_content if format_log_entry(log_entry) is not None]

    # Create unique filenames with date and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filtered_output_file = f"{os.path.splitext(filtered_output_file)[0]}[{timestamp}].txt"
    all_output_file = f"{os.path.splitext(all_output_file)[0]}[{timestamp}].txt"

    # Write the formatted results to the new files
    with open(filtered_output_file, 'w') as f:
        for log_entry in filtered_logs:
            f.write(log_entry + "\n")

    with open(all_output_file, 'w') as f:
        for log_entry in all_logs:
            f.write(log_entry + "\n")

    return filtered_output_file, all_output_file

if __name__ == "__main__":
    # Check that there is exactly one argument (the filename)
    if len(sys.argv) != 2:
        print("Usage: python format_log.py log_file.log")
        sys.exit(1)

    # Get the filename from the command line
    input_file = sys.argv[1]

    # Specify the filenames for the new files
    filtered_output_file = f"{os.path.splitext(input_file)[0]}_formatted_filtered"
    all_output_file = f"{os.path.splitext(input_file)[0]}_all_formatted"

    # Format the log file
    filtered_filename, all_filename = format_and_analyze_logs(input_file, filtered_output_file, all_output_file)

    # Print messages that the new files have been created
    print(f"Filtered formatted log file created: {filtered_filename}")
    print(f"All formatted log file created: {all_filename}")

import json
import sys
import os


def get_available_filename(base_filename):
    # Function to generate an available filename with incremental numbering
    if not os.path.exists(base_filename):
        return base_filename

    # If the file already exists, increment the number until an available file is found
    index = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}_{index}.txt"
        if not os.path.exists(new_filename):
            return new_filename
        index += 1


def format_log(input_file, output_file):
    # Read the content of the log file and split it into lines
    with open(input_file, 'r') as f:
        log_content = f.read().splitlines()

    formatted_logs = []

    # Loop through each log entry in the file
    for log_entry in log_content:
        try:
            # Try to decode the log entry as JSON
            log_json = json.loads(log_entry)
            log_level = log_json.get("level", -1)

            # Check if the log level is 3 or 4
            if log_level in [3, 4]:
                # Set a label based on the log level
                level_label = "ERROR" if log_level == 3 else "FATAL"

                # Add the formatted log entry to the list
                formatted_logs.append({
                    "level": level_label,
                    "time": log_json["time"],
                    "user": log_json["user"],
                    "method": log_json["method"],
                    "url": log_json["url"],
                    "message": log_json["message"]
                })
        except json.JSONDecodeError as e:
            # Print an error message if JSON decoding fails
            print(f"Error decoding JSON: {e}")

    # Generate an available filename for the formatted log file
    output_file = get_available_filename(output_file)

    # Write the formatted log entries to the new file
    with open(output_file, 'w') as f:
        for formatted_log in formatted_logs:
            # Write the log level and information for each log entry
            f.write(f"Level: {formatted_log['level']}\n")
            f.write(
                f"Time: {formatted_log['time']} - User: {formatted_log['user']}, Method: {formatted_log['method']}, URL: {formatted_log['url']}, Message: {formatted_log['message']}\n\n")


if __name__ == "__main__":
    # Check that there is exactly one argument (the file name)
    if len(sys.argv) != 2:
        print("Usage: python convert_log.py log_file.log")
        sys.exit(1)

    # Get the file name from the command line
    input_file = sys.argv[1]

    # Set the output file name (created in the same directory as the script is run from)
    output_file = "formatted_logfile.txt"

    # Get the available filename
    available_filename = get_available_filename(output_file)

    # Call the format_log function with the given file names
    format_log(input_file, available_filename)

    # Print a message indicating that the formatted log file has been created
    print(f"Formatted log file created: {available_filename}")


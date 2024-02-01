import json
import sys
import os
from datetime import datetime

def get_available_filename(base_filename):
    # Funktion för att generera ett tillgängligt filnamn med inkrementellt numrering
    if not os.path.exists(base_filename):
        return base_filename

    # Om filen redan finns, öka numret tills ett tillgängligt filnamn hittas
    index = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}_{index}.txt"
        if not os.path.exists(new_filename):
            return new_filename
        index += 1

def format_log(log_content, level_filter=None):
    formatted_logs = []

    # Loopa igenom varje loggpost i filen
    for log_entry in log_content:
        try:
            # Försök avkoda loggposten som JSON
            log_json = json.loads(log_entry)
            log_level = log_json.get("level", -1)

            # Om level_filter är angivet, filtrera efter loggnivå
            if level_filter is not None and log_level != level_filter:
                continue

            # Skapa en formaterad loggpost och lägg till den i listan
            formatted_logs.append({
                "level": log_json.get("level"),
                "time": log_json.get("time"),
                "user": log_json.get("user"),
                "method": log_json.get("method"),
                "url": log_json.get("url"),
                "message": log_json.get("message")
            })
        except json.JSONDecodeError as e:
            # Skriv ut ett felmeddelande om JSON-avkodning misslyckas
            print(f"Error decoding JSON: {e}")

    return formatted_logs

def format_and_analyze_logs(input_file, filtered_output_file, all_output_file):
    with open(input_file, 'r') as f:
        log_content = f.read().splitlines()

    # Formatera loggfilen med level-filter
    filtered_logs = format_log(log_content, level_filter=3)

    # Formatera hela loggfilen
    all_logs = format_log(log_content)

    # Skapa unika filnamn med datum och klockslag
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filtered_output_file = f"{os.path.splitext(filtered_output_file)[0]}[{timestamp}].txt"
    all_output_file = f"{os.path.splitext(all_output_file)[0]}[{timestamp}].txt"

    # Skriv de formaterade resultaten till de nya filerna
    with open(filtered_output_file, 'w') as f:
        for log_entry in filtered_logs:
            f.write(json.dumps(log_entry) + "\n")

    with open(all_output_file, 'w') as f:
        for log_entry in all_logs:
            f.write(json.dumps(log_entry) + "\n")

    return filtered_output_file, all_output_file

if __name__ == "__main__":
    # Kontrollera att det finns exakt ett argument (filnamnet)
    if len(sys.argv) != 2:
        print("Användning: python format_log.py loggfil.log")
        sys.exit(1)

    # Hämta filnamnet från kommandoraden
    input_file = sys.argv[1]

    # Ange filnamnen för de nya filerna
    filtered_output_file = f"{os.path.splitext(input_file)[0]}_formatted_filtered"
    all_output_file = f"{os.path.splitext(input_file)[0]}_all_formatted"

    # Formatera loggfilen
    filtered_filename, all_filename = format_and_analyze_logs(input_file, filtered_output_file, all_output_file)

    # Skriv ut meddelanden om att de nya filerna har skapats
    print(f"Filtered formatted log file created: {filtered_filename}")
    print(f"All formatted log file created: {all_filename}")

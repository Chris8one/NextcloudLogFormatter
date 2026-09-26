import openai
import sys
import os
from datetime import datetime

def get_openai_key():
    with open("openai_key.txt", "r") as key_file:
        return key_file.read().strip()

def get_available_filename(base_filename):
    if not os.path.exists(base_filename):
        return base_filename

    index = 1
    while True:
        new_filename = f"{os.path.splitext(base_filename)[0]}_{index}.txt"
        if not os.path.exists(new_filename):
            return new_filename
        index += 1

def analyze_errors_with_openai(error_messages):
    openai.api_key = get_openai_key()
    questions = ["Vad kan orsaka detta fel?", "Finns det en lösning på detta problem?"]
    answers = []

    for error_message in error_messages:
        question = f"För felmeddelandet: {error_message}. {questions[0]}"
        response = openai.Completion.create(
            engine="gpt-3.5-turbo-instruct",
            prompt=question,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None
        )

        answers.append({
            "error_message": error_message,
            "question": question,
            "answer": response.choices[0].text.strip()
        })

    analysis_filename = f"analyzed_log[{datetime.now().strftime('%Y%m%d_%H%M%S')}].txt"
    with open(analysis_filename, 'w') as f:
        for answer in answers:
            f.write(f"For error message: {answer['error_message']}\n")
            f.write(f"Question: {answer['question']}\n")
            f.write(f"Answer: {answer['answer']}\n\n")

    return analysis_filename

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Ange filnamnet som ett argument. Exempel: python format_log_chatgpt.py nextcloud.log")
        sys.exit(1)

    input_file = sys.argv[1]
    with open(input_file, 'r') as f:
        error_messages = f.read().splitlines()

    analysis_filename = analyze_errors_with_openai(error_messages)
    print(f"Analysis file created: {analysis_filename}")

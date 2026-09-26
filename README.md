# Nextcloud Log Formatter

A Python command-line tool that reads raw Nextcloud log files and converts JSON log entries into a more readable text format.

The tool creates one file containing all formatted log entries and another file containing only critical entries with log level `3` or `4` (`ERROR` and `FATAL`).

## Background

This tool was developed during my internship to simplify log analysis in an IT operations environment.

Nextcloud log files can contain large amounts of JSON data that are difficult to review manually. The purpose of this project was to make the information easier to read and help identify serious errors more quickly.

## Features

* Reads Nextcloud log files containing JSON entries
* Converts numeric log levels into readable names
* Extracts useful information from each log entry
* Creates a formatted file containing all log entries
* Creates a separate file containing only `ERROR` and `FATAL` entries
* Adds a timestamp to generated filenames
* Displays parsing errors when invalid JSON is encountered

The following information is extracted when available:

* Log level
* Request ID
* Time
* Remote address
* User
* Application
* HTTP method
* URL
* Message
* User agent
* Exception information
* Additional data
* Nextcloud version

## Technologies

* Python
* JSON parsing
* File handling
* Command-line arguments
* Date and time handling

The main formatter uses only modules from the Python standard library and does not require external packages.

## Project structure

* `format_log.py` – the main log formatting tool
* `experiments/ai_log_analysis_prototype.py` – an unfinished experiment for AI-assisted error analysis
* `requirements.txt` – dependencies used by the experimental AI prototype

## Requirements

To run the main formatter, you need:

* Python 3
* A Nextcloud log file containing one JSON object per line

No external Python packages are required for the main formatter.

## Usage

Run the script from a terminal and provide the path to a Nextcloud log file:

```bash
python3 format_log.py nextcloud.log
```

On Windows, the command may instead be:

```bash
python format_log.py nextcloud.log
```

You can also provide a complete path to the log file:

```bash
python3 format_log.py /path/to/nextcloud.log
```

## Output

The script creates two text files in the current directory.

### Filtered output

The filtered file contains only entries with log level `3` or `4`:

* `ERROR`
* `FATAL`

Example filename:

```text
nextcloud_formatted_filtered[20260926_193000].txt
```

### Complete output

The complete file contains all successfully formatted log entries:

```text
nextcloud_all_formatted[20260926_193000].txt
```

## Example

A simplified Nextcloud log entry may look like this:

```json
{
  "reqId": "abc123",
  "level": 3,
  "time": "2026-09-26T17:30:00+00:00",
  "remoteAddr": "192.0.2.1",
  "user": "example-user",
  "app": "files",
  "method": "GET",
  "url": "/remote.php/dav/files/example-user/",
  "message": "Example error message",
  "userAgent": "Example client",
  "version": "28.0.0"
}
```

The formatted output becomes easier to review:

```text
ERROR
Request Id: abc123
Time: 2026-09-26T17:30:00+00:00
Remote Address: 192.0.2.1
User: example-user
App: files
Method: GET
URL: /remote.php/dav/files/example-user/
Message: Example error message
User Agent: Example client
Exception: None
Data: None
Version: 28.0.0
```

## Experimental AI analysis

The `experiments` directory contains an early prototype for analysing error messages with an AI service.

This prototype is not part of the main formatter and should be considered unfinished. It was created to explore whether AI could help explain possible causes and solutions for errors found in Nextcloud logs.

The prototype uses an older version of the OpenAI Python library and an older API implementation. It may require changes before it can be used with current APIs and models.

The dependencies in `requirements.txt` belong primarily to this experimental prototype and are not required by the main formatter.

## Current limitations

* The program expects one valid JSON object per line
* A malformed JSON entry may interrupt processing
* Input and output filenames are provided through the command line
* Log levels are currently fixed to Nextcloud levels `3` and `4`
* There are currently no automated tests
* The experimental AI prototype is unfinished
* The experimental AI integration uses an older API implementation

These limitations are documented because the main formatter has not been changed or retested since its original use.

## Security and privacy

Nextcloud logs may contain sensitive information such as:

* Usernames
* IP addresses
* File paths
* Request information
* Internal URLs
* Error and exception details

Do not upload real production logs or generated output files to a public repository. Use anonymised example data when demonstrating or testing the tool.

API keys must never be committed to source control. The experimental prototype reads its key from a local file named `openai_key.txt`. That file must remain local and must not be uploaded to GitHub.

## Possible future improvements

* Improve handling of malformed JSON entries
* Process each log entry only once
* Add command-line options for selecting log levels
* Add automated tests
* Add anonymisation of usernames and IP addresses
* Add an anonymised example log file
* Update or replace the experimental AI integration
* Separate the experimental dependencies from the main project

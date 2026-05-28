#idea here is to automate ffuf at scale. 
import subprocess
import sys
import base64
import pickle
import inspect
import keyword
from pathlib import Path

#so now to think of how to do this at scale. ideally you'd line up the targets and wordlists, and then script them to run concurrenly, and then digest the results. If we're looking for something specific, we can digest against that, or we can just have a big list of results to go through.
def ffuf_scan(target_url,  wordlist_path, output_path, header=None, mode=None):
    command = [
        "ffuf",
        "-u", target_url,
    ]
    if header:
        command.extend(["-H", header])
    if mode:
        command.extend(["-mode", mode])
    command.extend([
        "-w", wordlist_path,
        "-o", output_path,
        "-of", "json"
    ])
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Scan completed successfully. Output saved to {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running ffuf: {e.stderr}", file=sys.stderr)
""" 
Usage:
    ffuf_scan("http://example.com/FUZZ", "path/to/wordlist.txt", "output.json")
This function will run ffuf with the specified target URL, wordlist, and output path. The results will be saved in JSON format for easy parsing and analysis.
"""

def digest_ffuf_results(json_path):
    import json
    with open(json_path, 'r') as f:
        data = json.load(f)
    results = []
    for item in data.get('results', []):
        result = {
            'url': item.get('url'),
            'status': item.get('status'),
            'length': item.get('length'),
            'words': item.get('words'),
            'lines': item.get('lines')
        }
        results.append(result)
    return results
"""
Usage:
    results = digest_ffuf_results("output.json")
    for result in results:
        print(result)
This function reads the JSON output from ffuf and extracts relevant information such as the URL, status code, response length, word count, and line count. The results are returned as a list of dictionaries for easy access and further processing.
"""

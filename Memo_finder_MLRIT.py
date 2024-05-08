"""
# Requirements:
- pymupdf
- requests


# Instructions:
- Run the script
- Enter your roll number
- Enter the starting range of memo numbers to check
- Enter the ending range of memo numbers to check
- The script will check all the memo numbers in the range you provided and will stop when it finds the memo with your roll number

# Note:
- The script will download the PDFs in the data folder
- The script will stop as soon as it finds the memo with your roll number

# Disclaimer:
- This script is for educational purposes only

# Author:
- Rishikesh Reddy A

# About the Script:

- This script is used to find the memo number of a student in MLRIT.
- The script will download the PDFs of the memos and check if the memo contains the roll number of the student.
- The script will stop as soon as it finds the memo with the roll number of the student.
"""


import fitz
import requests
import os
import shutil
import multiprocessing as mp

src_dir = "data"

if not os.path.exists(src_dir):
    os.makedirs(src_dir)

def load_doc(file_path):
    doc = fitz.open(file_path)
    return doc

def extract_text(doc):
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def download_file(url):
    local_filename = f"{src_dir}/{url.split('/')[-1]}"
    with requests.get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    return local_filename

def work(i):
    print(f"Checking {i}")
    url = f"https://exams.mlrinstitutions.ac.in/MarksMemo/{i}.pdf"
    file = download_file(url)
    try:
        doc = load_doc(file)
    except fitz.FileDataError as e:
        print(f"Memo {i} Not Found Skipping")
        return None, False
    text = extract_text(doc)
    doc.close()
    if "20R21A67" in text:
        return i, True
        
    else:
        return None, False


def callback(t):
    i, found = t
    if found:
        print(f"\n\n\n\nFound the memo at https://exams.mlrinstitutions.ac.in/MarksMemo/{i}.pdf\n\n\n\n")
        pool.terminate()
        pool.join()
        return
    
if __name__ == "__main__":
    roll = input("Enter your roll number (All Caps):  ")
    start = int(input("Select the starting range of Memo Numbers to check:   "))
    end = int(input("Select the ending range of Memo Numbers to check:   "))
    pool = mp.Pool(mp.cpu_count())
    check_range = range(start, end)
    for i in check_range:
        pool.apply_async(work, args=(i,), callback=callback)
    pool.close()
    pool.join()
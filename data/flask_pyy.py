from flask import Flask, jsonify
import json
import os
import requests
from bs4 import BeautifulSoup

url = "https://services.gov.im/job-search/results"  # Change this to your actual API endpoint

# Custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Sending a GET request to the APIhttps://github.com/HammerThunderr/manxall/edit/main/data/flask_pyy.py
response = requests.get(url, headers=headers)

# Print raw response content and status code
print("Response Status Code:", response.status_code)
print("Raw response content:", response.text[:500])  # Print the first 500 characters of the response

# Check if the request was successful
if response.status_code == 200:
    print("aaaaaa")  # Debugging checkpoint

    # Parse the HTML content
    try:
        bs4 = BeautifulSoup(response.text, 'lxml')
        print("Parsing successful.")  # Debugging checkpoint

        # List to hold job data
        jobs = []

        # Extract job listings (verify if 'tr' elements exist)
        rows = bs4.find_all('tr')
        print("Number of rows found:", len(rows))

        for row in rows[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) >= 4:  # Ensure there are enough columns
                job_id = columns[0].get_text(strip=True)
                job_description = columns[1].get_text(strip=True)
                employer = columns[2].get_text(strip=True)
                hours = columns[3].get_text(strip=True)

                # Append job data to the list
                jobs.append({
                    "Job ID": job_id,
                    "Job Description": job_description,
                    "Employer": employer,
                    "Hours": hours
                })
            else:
                print("Skipping a row due to insufficient columns:", row)

        # Convert the extracted job data to JSON format
        json_data = json.dumps(jobs, indent=4)
       # print(json_data)  # Print or save your JSON data here
        print("eeeeee")  # Print or save your JSON data here
        # Ensure the 'data' directory exists
        os.makedirs('data', exist_ok=True)

        # Save JSON data to a file
        with open('data/latest_data.json', 'w', encoding='utf-8') as json_file:
            json_file.write(json_data)  # This line should be indented to be inside the 'with' block
        print("JSON data saved to data/latest_data.json")


  
        

    

    except Exception as e:
        print(f"An error occurred during parsing: {e}")
else:
    print(f"Failed to retrieve data: {response.status_code}")

app = Flask(__name__)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    print("ffffff")
    # Check if the JSON file exists
    if os.path.exists('data/latest_data.json'):
        with open('data/latest_data.json', 'r', encoding='utf-8') as json_file:
            job_data = json.load(json_file)
        return jsonify(job_data), 200
    else:
        return jsonify({"error": "No job listings available."}), 404

if __name__ == '__main__':
    app.run(debug=True)

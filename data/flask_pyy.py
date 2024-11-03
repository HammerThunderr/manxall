from flask import Flask, jsonify
import json
import os
import requests
from bs4 import BeautifulSoup

# Replace 'API_URL' with the actual URL of the API you want to scrape
url = "https://services.gov.im/job-search/results"  # Change this to your actual API endpoint

# Custom headers, including a User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
}

# Sending a GET request to the API
response = requests.get(url, headers=headers)

# Print raw response content and status code
print("Response Status Code:", response.status_code)
print("Raw response content:", response.text)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'lxml')

    # List to hold job data
    jobs = []

    # Extract job listings
    for row in soup.find_all('tr')[1:]:  # Skip the header row
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

    # Convert the extracted job data to JSON format
    json_data = json.dumps(jobs, indent=4)
    print(json_data)  # Print or save your JSON data here
     # Save JSON data to a file
    # Save JSON data to a file
    with open('job_listings.json', 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)
    print("JSON data saved to job_listings.json")

else:
    print(f"Failed to retrieve data: {response.status_code}")

app = Flask(__name__)

@app.route('/jobs', methods=['GET'])
def get_jobs():
    # Check if the JSON file exists
    if os.path.exists('job_listings.json'):
        with open('job_listings.json', 'r', encoding='utf-8') as json_file:
            job_data = json.load(json_file)
        return jsonify(job_data), 200  # Return JSON data with HTTP 200 status
    else:
        return jsonify({"error": "No job listings available."}), 404  # Return error if file doesn't exist

if __name__ == '__main__':
    app.run(debug=True)  # Run the Flask app in debug mode

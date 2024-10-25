from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options  # Needed for headless mode
from bs4 import BeautifulSoup
import requests
import time

# Set up ChromeDriver with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Enable headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set up the ChromeDriver service with the path to ChromeDriver
service = Service("/Users/louis.rushton/Downloads/chromedriver-mac-arm64/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the webpage
driver.get("https://nbafantasy.nba.com/leagues/6768/standings/c")

# Wait for the page to fully load
time.sleep(5)  # Adjust the delay based on your internet speed

# Get the page source after it's fully rendered
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Now, try finding the standings table
standings_table = soup.find('table', {'class': 'Table-sc-g4vec0-1'})

standings_data = ""
if standings_table:
    rows = standings_table.find_all('tr')
    standings = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns:
            team_name = columns[1].find('strong').text.strip()  # Extract the team name
            manager_name = columns[1].contents[2].strip()  # Extract the manager name
            gd = columns[2].text.strip()  # Extract GD value
            tot = columns[3].text.strip()  # Extract TOT value
            standings.append(f"{team_name} ({manager_name}): GD={gd}, TOT={tot}")
    
    # Format the standings output
    standings_data = "\n".join(standings)
    print("NBA Fantasy League Standings:\n")
    print(standings_data)
else:
    standings_data = "Standings table not found!"
    print(standings_data)

# Close the browser
driver.quit()

# Zapier webhook URL
zapier_webhook_url = 'https://hooks.zapier.com/hooks/catch/20533683/291p5b4/'

# Send the standings data to the Zapier webhook
response = requests.post(zapier_webhook_url, json={"standings": standings_data})

# Check if the POST request was successful
if response.status_code == 200:
    print("Standings data sent to Zapier successfully!")
else:
    print(f"Failed to send data to Zapier. Status code: {response.status_code}")

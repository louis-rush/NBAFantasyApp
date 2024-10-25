from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

# Update this path to point to the actual executable, not the folder
service = Service("/Users/louis.rushton/Downloads/chromedriver-mac-arm64/chromedriver")

# Start the WebDriver with the correct path to ChromeDriver
driver = webdriver.Chrome(service=service)

# Load the webpage
driver.get("https://nbafantasy.nba.com/leagues/6768/standings/c")

# Wait for the page to fully load
time.sleep(5)  # You may need to adjust this delay based on your internet speed

# Get the page source after it's fully rendered
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

# Now, try finding the standings table
standings_table = soup.find('table', {'class': 'Table-sc-g4vec0-1'})

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
    print("Standings table not found!")

# Close the browser
driver.quit()

import pandas as pd
from bs4 import BeautifulSoup
import requests

url = 'https://www.infolinkuniversity.net/'
response  = requests.get(url)

content = response.text

soup = BeautifulSoup(content,'html.parser')

table = soup.find('table')  # Find the first table
headers = [th.text.strip() for th in table.find_all('th')]  
rows = []

# Extract table rows
for row in table.find_all('tr'):
    cells = [td.text.strip() for td in row.find_all('td')]
    if cells:  # Skip empty rows
        rows.append(cells)

# Step 4: Create a pandas DataFrame
df = pd.DataFrame(rows, columns=headers)

# Step 5: Save the DataFrame to an Excel file
output_file = "output.xlsx"
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Data saved to {output_file}")



from bs4 import BeautifulSoup
import requests
import pandas as pd

def print_grid_from_webpage(url):

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        table = soup.find('table')

        data = []
        rows = table.find_all('tr')
        for i, row in enumerate(rows):
            if i == 0:
                continue
            columns = row.find_all('td')
            x = int(columns[0].text.strip())
            char = columns[1].text.strip()
            y = int(columns[2].text.strip())
            data.append([x, char, y])

        df = pd.DataFrame(data, columns=['x-coordinate', 'Character', 'y-coordinate'])

        max_x = df['x-coordinate'].max()
        max_y = df['y-coordinate'].max()

        grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

        for index, row in df.iterrows():
            x = row['x-coordinate']
            y = row['y-coordinate']
            char = row['Character']
            grid[max_y - y][x] = char

        for row in grid:
            print(''.join(row))

    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
print_grid_from_webpage(url)

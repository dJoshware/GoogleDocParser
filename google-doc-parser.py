import requests
from bs4 import BeautifulSoup


def fetch_and_parse_doc(url):
    # Fetch document content
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    # get_text(separator=", ") - separates page content via comma into substrings
    content = soup.get_text(separator=", ").split(", ")
    # .split(", ") - creates list of the substrings
    return content


def group_coordinates_from_first_number(content):
    coordinates = [] # empty list to append coordinates to
    
    # Find the index of the first numeric value
    start_index = next(i for i, item in enumerate(content) if item.isdigit())
    
    # Group items in threes from the first numeric index onward
    for i in range(start_index, len(content), 3):
        try:
            x = int(content[i].strip())
            char = content[i + 1].strip()
            y = int(content[i + 2].strip())
            coordinates.append({"x": x, "y": y, "char": char})
        except (IndexError, ValueError):
            # Break if there are insufficient items to form a group of three
            break
    
    return coordinates


def build_and_print_grid(coordinates):
    # Determine grid size
    max_x = max(coord['x'] for coord in coordinates)
    max_y = max(coord['y'] for coord in coordinates)

    # Initialize grid with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Populate grid with characters
    for coord in coordinates:
        x, y, char = coord['x'], coord['y'], coord['char']
        grid[y][x] = char

    # Print grid
    for row in reversed(grid):
        print(''.join(row))


# Usage
# url = "https://docs.google.com/document/d/e/2PACX-1vRMx5YQlZNa3ra8dYYxmv-QIQ3YJe8tbI3kqcuC7lQiZm-CSEznKfN_HYNSpoXcZIV3Y_O3YoUB1ecq/pub"
url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

doc_content = fetch_and_parse_doc(url)
coordinates = group_coordinates_from_first_number(doc_content)
build_and_print_grid(coordinates)

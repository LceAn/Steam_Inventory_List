import csv
import re
from bs4 import BeautifulSoup

# --- Configuration ---
INPUT_HTML_FILE = 'index.html'
OUTPUT_CSV_FILE = 'steam_games.csv'

def parse_game_data(html_content):
    """
    Parses the provided HTML content to extract game data based on the specific
    class names found in your index.html file.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    games_data = []

    # 1. Find all game rows using the correct parent class name you provided.
    # The class name is '_2-pQFn1G7dZ7667rrakcU3' and seems to wrap each game.
    game_rows = soup.find_all('div', class_='_2-pQFn1G7dZ7667rrakcU3')

    if not game_rows:
        print("❌ Error: Could not find any game elements with the class '_2-pQFn1G7dZ7667rrakcU3'.")
        print("Please ensure the HTML file contains the data as provided.")
        return []

    print(f"✅ Found {len(game_rows)} game entries. Now extracting details...")

    # 2. Loop through each game row and extract the details.
    for row in game_rows:
        try:
            # Find the game name. It's in an 'a' tag with class '_22awlPiAoaZjQMqxJhp-KP'.
            name_element = row.find('a', class_='_22awlPiAoaZjQMqxJhp-KP')
            name = name_element.text.strip() if name_element else 'Unknown Game'

            # Find the playtime. It's in a 'span' with class '_26nl3MClDebGDV7duYjZVn'.
            hours_element = row.find('span', class_='_26nl3MClDebGDV7duYjZVn')
            hours_text = hours_element.text.strip() if hours_element else '0'
            
            # Use regex to reliably extract the number (digits, commas, and dots).
            match = re.search(r'[\d,]+\.?\d*', hours_text.replace(',', ''))
            hours = float(match.group(0)) if match else 0.0

            games_data.append({'title': name, 'hours': hours})
        except Exception as e:
            print(f"⚠️ Warning: Could not parse a row. Skipping. Error: {e}")

    return games_data

def save_to_csv(data, filename):
    """Saves the extracted data to a CSV file."""
    if not data:
        print("No data was extracted to save.")
        return

    # Sort the data by hours played, from most to least.
    data.sort(key=lambda x: x['hours'], reverse=True)

    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['title', 'hours']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"\n🎉 Success! All data has been saved to '{filename}'.")
    print("You can now open this file with Excel, Google Sheets, or Apple Numbers.")

def main():
    """Main execution function."""
    try:
        with open(INPUT_HTML_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"❌ Error: Input file '{INPUT_HTML_FILE}' not found. Make sure it's in the same folder as the script.")
        return
    
    parsed_data = parse_game_data(html_content)
    save_to_csv(parsed_data, OUTPUT_CSV_FILE)

if __name__ == '__main__':
    main()
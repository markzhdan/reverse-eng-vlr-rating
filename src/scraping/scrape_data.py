# Reverse engineering VLR player rating
# Purpose: To reverse engineer the VLR.gg player rating calculation using their stat data.
# File: scrape_data.py - used to parse vlr stats pages and store raw data.
# Mark Zhdan | 01-05-2023

import requests
from bs4 import BeautifulSoup
import pandas as pd

# URLs that contain stats
base_url = "https://www.vlr.gg"
pages = {
    "champions2023": "/event/stats/1657/valorant-champions-2023",
    "stats_alltime": "/stats/?event_group_id=all&event_id=all&region=all&country=all&min_rounds=1000&min_rating=1550&agent=all&map_id=all&timespan=all",
    "stats_recent": "/stats",
    "season2023": "/stats/?event_group_id=45&event_id=all&region=all&country=all&min_rounds=400&min_rating=1550&agent=all&map_id=all&timespan=all",
}

for page_name, path in pages.items():
    try:
        response = requests.get(base_url + path)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, "html.parser")

        table = soup.find("table", class_="wf-table mod-stats mod-scroll")
        headers = [header.text.strip() for header in table.find_all("th")]

        data = []
        # Exclude "Agents" column (fixes data shifting)
        if "Agents" in headers:
            agents_index = headers.index("Agents")
            headers.pop(agents_index)

            for row in table.find_all("tr")[1:]:
                row_data = []
                for i, col in enumerate(row.find_all("td")):
                    if i != agents_index:
                        row_data.append(col.text.strip())

                data.append(row_data)
        else:
            for row in table.find_all("tr")[1:]:
                row_data = [col.text.strip() for col in row.find_all("td")]

                data.append(row_data)

        df = pd.DataFrame(data, columns=headers)
        csv_file = f"data/raw/{page_name}.csv"
        df.to_csv(csv_file, index=False)

        print(f"Saved data into {csv_file}")

    except requests.RequestException as e:
        print(f"Failed to retrieve data for {page_name}: {e}")

print("\nScraping data for all pages completed.")

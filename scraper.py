import itertools
import time

import pandas as pd


BASE_URL = "https://bolsholeinone.com/wall-of-fame/?wpv-wpcf-date_min-format=Y-m-d&wpv-wpcf-date_max-format=Y-m-d&wpv_view_count=24-TCPID59&wpv-wpcf-first-name=&wpv-wpcf-golfclub=&wpv-wpcf-country=&wpv-wpcf-date_min=&wpv-wpcf-date_min-format=Y-m-d&wpv-wpcf-date_max=&wpv-wpcf-date_max-format=Y-m-d&wpv_paged="


def get_data():
    """Get hole in ones from Bols hole in one website.
    """
    dfs = list()
    for i in itertools.count(1):
        print(i)  # Show progress
        url = BASE_URL + str(i)
        try:
            new_df = pd.read_html(url)
            dfs += new_df
        except:
            print(f'Scraped {i-1} pages.')
            break

    # Combine all pages into one dataframe.
    df = pd.concat(dfs)

    # Show output
    pd.set_option('display.max_columns', None)
    print(df.head())

    # Save to file.
    timestamp = int(time.time())
    df.to_csv(f"{timestamp}.csv", index=False)


if __name__ == '__main__':
    get_data()

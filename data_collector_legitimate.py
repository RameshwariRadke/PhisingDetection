import requests as re
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from urllib.parse import urlparse
import os
import time

from bs4 import BeautifulSoup
import pandas as pd
import feature_extraction as fe

disable_warnings(InsecureRequestWarning)

# LOAD URL LIST
url_file = 'mini_dataset/tranco_2N6P9.csv'
data_frame = pd.read_csv(url_file, header=None, names=['rank', 'url'])
url_list = data_frame['url'].astype(str).tolist()

# URL CLEANER
def clean_url(url):
    url = url.strip().lstrip(".")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # HTTPS FIRST

    parsed = urlparse(url)
    host = parsed.netloc

    if (
        not host or
        host.startswith(".") or
        host.endswith(".") or
        ".." in host or
        "." not in host
    ):
        return None

    return url

# RANGE SELECTION
begin = 30000
end = 30100
collections_list = url_list[begin:end]

collections_list = [clean_url(url) for url in collections_list]
collections_list = [url for url in collections_list if url is not None]

# REQUEST SESSION
session = re.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

# SCRAPING FUNCTION
def create_structured_data(url_list):
    data_list = []

    for idx, url in enumerate(url_list):
        try:
            response = session.get(
                url,
                timeout=6,
                verify=False,
                allow_redirects=True
            )

            if response.status_code not in [200, 301, 302]:
                print(idx, "Skipped (status)", response.status_code, url)
                continue

            final_url = response.url
            if clean_url(final_url) is None:
                print(idx, "Skipped (bad redirect)", final_url)
                continue

            soup = BeautifulSoup(response.content, "html.parser")
            vector = fe.create_vector(soup)

            if vector is None or len(vector) == 0:
                print(idx, "Skipped (empty features)", final_url)
                continue

            vector.append(final_url)
            data_list.append(vector)

        except re.exceptions.RequestException as e:
            print(idx, "Request failed:", e)
            continue

        time.sleep(0.5)  # RATE LIMIT (IMPORTANT)

    return data_list

# RUN COLLECTION
data = create_structured_data(collections_list)

# DATAFRAME
columns=['has_title',
         'has_input',
         'has_image',
         'has_button',
         'has_submit',
         'has_link',
         'has_password',
         'has_email_input',
         'has_hidden_element',
         'has_audio',
         'has_video',
         'number_of_inputs',
         'number_of_images',
         'number_of_buttons',
         'number_of_options',
         'number_of_list',
         'number_of_th',
         'number_of_tr',
         'number_href',
         'number_paragraph',
         'number_of_script',
         'number_of_title',
         'has_h1',
         'has_h2',
         'has_h3',
         'length_of_text',
         'number_of_clickable_button',
         'number_of_a',
         'number_of_img',
         'number_of_div',
         'number_of_figure',
         'has_footer',
         'has_form',
         'has_text_area',
         'has_iframe',
         'has_text_input',
         'number_of_meta',
         'has_nav',
         'has_object',
         'has_picture',
         'number_of_sources',
         'number_of_span',
         'number_of_table',
         'URL']

df = pd.DataFrame(data=data, columns=columns)
df['label'] = 0  # legit

file_path = "structured_data_legitemate.csv"

if not os.path.exists(file_path):
    df.to_csv(file_path, index=False)
else:
    df.to_csv(file_path, mode='a', header=False, index=False)

print("Collected rows:", len(df))





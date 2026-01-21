from bs4 import BeautifulSoup

# -------------------------
# BASIC PRESENCE FEATURES
# -------------------------

def has_title(soup):
    return 1 if soup.title and soup.title.text.strip() else 0


def has_input(soup):
    return 1 if soup.find("input") else 0


def has_button(soup):
    return 1 if soup.find("button") else 0


def has_submit(soup):
    return 1 if soup.find("input", {"type": "submit"}) else 0


def has_image(soup):
    return 1 if soup.find("img") else 0


def has_link(soup):
    # Hyperlinks, not <link> tags
    return 1 if soup.find("a", href=True) else 0


def has_password(soup):
    return 1 if soup.find("input", {"type": "password"}) else 0


def has_email_input(soup):
    return 1 if soup.find("input", {"type": "email"}) else 0


def has_hidden_element(soup):
    return 1 if soup.find("input", {"type": "hidden"}) else 0


def has_audio(soup):
    return 1 if soup.find("audio") else 0


def has_video(soup):
    return 1 if soup.find("video") else 0


# -------------------------
# COUNT-BASED FEATURES
# -------------------------

def number_of_inputs(soup):
    return len(soup.find_all("input"))


def number_of_images(soup):
    return len(soup.find_all("img"))


def number_of_buttons(soup):
    return len(soup.find_all("button"))


def number_of_option(soup):
    return len(soup.find_all("option"))


def number_of_list(soup):
    return len(soup.find_all("li"))


def number_of_th(soup):
    return len(soup.find_all("th"))


def number_of_tr(soup):
    return len(soup.find_all("tr"))


def number_href(soup):
    # Count actual hyperlinks
    return len(soup.find_all("a", href=True))


def number_paragraph(soup):
    return len(soup.find_all("p"))

# number_of_scripts
def number_of_script(soup):
    return len(soup.find_all("script"))

# number_of_title
def number_of_title(soup):
    # Count title tags, not characters
    return len(soup.find_all("title"))

# has_h1
def has_h1(soup):
    if len(soup.find_all("h1"))>0:
        return 1
    else:
        return 0

# has_h2
def has_h2(soup):
    if len(soup.find_all("h2"))>0:
        return 1
    else:
        return 0

# has_h3
def has_h3(soup):
    if len(soup.find_all("h3"))>0:
        return 1
    else:
        return 0

#length_of_text
def length_of_text(soup):
    return len(soup.get_text())

#number_of_clickable_button
def number_of_clickable_button(soup):
    count=0
    for button in soup.find_all("button"):
        if button.get("type")=="button":
            count+=1
        return count
def number_of_a(soup):
    return len(soup.find_all("a"))

def number_of_img(soup):
    return len(soup.find_all("img"))

def number_of_div(soup):
    return len(soup.find_all("div"))

def number_of_figure(soup):
    return len(soup.find_all("figure"))

def has_footer(soup):
    if len(soup.find_all("footer"))>0:
        return 1
    else:
        return 0

def has_text_area(soup):
    if len(soup.find_all("text"))>0:
        return 1
    else:
        return 0
def has_form(soup):
    if len(soup.find_all("form"))>0:
        return 1
    else:
        return 0

def has_iframe(soup):
    if len(soup.find_all("iframe"))>0:
        return 1
    else:
        return 0

def has_text_input(soup):
    for input in soup.find_all("input"):
        if input.get("type")=="text":
            return 1
    return 0

def number_of_meta(soup):
    return len(soup.find_all("meta"))

def has_nav(soup):
    if len(soup.find_all("nav"))>0:
        return 1
    else:
        return 0

def has_object(soup):
    if len(soup.find_all("object"))>0:
        return 1
    else:
        return 0

def has_picture(soup):
    if len(soup.find_all("picture"))>0:
        return 1
    else:
        return 0
def number_of_sources(soup):
    return len(soup.find_all("source"))

def number_of_span(soup):
    return len(soup.find_all("span"))

def number_of_table(soup):
    return len(soup.find_all("table"))

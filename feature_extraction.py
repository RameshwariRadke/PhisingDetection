from bs4 import BeautifulSoup
import os
import feature as fe
import pandas as pd

file_name="mini_dataset/8.html"

## Define a function that opens HTML files and returns the content
def open_file(file_name):
    with open(file_name,"r",encoding="utf-8", errors="ignore") as f:
        return f.read()
## Define a function to create beautifulsoup object
def creat_soup(text):
    return BeautifulSoup(text,"html.parser")

## Define a function that creates a vector by running all feature functions for the soup object
def create_vector(soup):
    return [
        fe.has_title(soup),
        fe.has_input(soup),
        fe.has_image(soup),
        fe.has_button(soup),
        fe.has_submit(soup),
        fe.has_link(soup),
        fe.has_password(soup),
        fe.has_email_input(soup),
        fe.has_hidden_element(soup),
        fe.has_audio(soup),
        fe.has_video(soup),
        fe.number_of_inputs(soup),
        fe.number_of_images(soup),
        fe.number_of_buttons(soup),
        fe.number_of_option(soup),
        fe.number_of_list(soup),
        fe.number_of_th(soup),
        fe.number_of_tr(soup),
        fe.number_href(soup),
        fe.number_paragraph(soup),
        fe.number_of_script(soup),
        fe.number_of_title(soup),
        fe.has_h1(soup),
        fe.has_h2(soup),
        fe.has_h3(soup),
        fe.length_of_text(soup),
        fe.number_of_clickable_button(soup),
        fe.number_of_a(soup),
        fe.number_of_img(soup),
        fe.number_of_div(soup),
        fe.number_of_figure(soup),
        fe.has_footer(soup),
        fe.has_form(soup),
        fe.has_text_area(soup),
        fe.has_iframe(soup),
        fe.has_text_input(soup),
        fe.number_of_meta(soup),
        fe.has_nav(soup),
        fe.has_object(soup),
        fe.has_picture(soup),
        fe.number_of_sources(soup),
        fe.number_of_span(soup),
        fe.number_of_table(soup)
    ]
## Run steps 1,2,3 for all the html files and create a 2d array

folder_name='mini_dataset'
def create_2d_list(folder_name):
    directory=os.path.join(os.getcwd(),folder_name)
    data=[]
    for file in sorted(os.listdir(directory)):
        soup=creat_soup(open_file(directory+"/"+file))
        data.append(create_vector(soup))
    return data

# ## Create dataframe by using 2D array
# data=create_2d_list(folder_name)
#
# columns=['has_title',
#          'has_input',
#          'has_image',
#          'has_button',
#          'has_submit',
#          'has_link',
#          'has_password',
#          'has_email_input',
#          'has_hidden_element',
#          'has_audio',
#          'has_video',
#          'number_of_inputs',
#          'number_of_images',
#          'number_of_buttons',
#          'number_of_options',
#          'number_of_list',
#          'number_of_th',
#          'number_of_tr',
#          'number_href',
#          'number_paragraph',
#          'number_of_script',
#          'number_of_title']
#
# df=pd.DataFrame(data=data,columns=columns)
#
# print(df.head())
from bs4 import BeautifulSoup
import re

def parsing (data_):
    soup_ = BeautifulSoup(data_, "html.parser")
    soup_ = soup_.find_all('pre')[1].get_text()
    tmp_ = re.split(r'\n\n', soup_)
    tmp_ = re.split(r'\n', tmp_[1])

    return tmp_[0]
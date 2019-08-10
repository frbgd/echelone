from bs4 import BeautifulSoup
import re

def parsing (data_):
    result_ = []
    soup_ = BeautifulSoup(data_, "html.parser")
    soup_ = soup_.find_all('pre')[1].get_text()
    tmp_ = re.split(r'\n\n', soup_)
    tmp_ = re.split(r'\n', tmp_[1])
    if len(tmp_) == 23:
        return result_
    tmp_ = re.split(r' ', tmp_[0])

    try:
        net_mask = tmp_[0]
    except:
        net_mask = 'NONE'
    try:
        via = tmp_[2]
    except:
        via = 'NONE'
    try:
        dev = tmp_[4]
    except:
        dev = 'NONE'
    try:
        fwmark = tmp_[6]
    except:
        fwmark = 'NONE'

    result_.append({"net_mask":net_mask, "via":via, "dev":dev, "fwmark":fwmark})

    return result_
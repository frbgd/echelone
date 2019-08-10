from bs4 import BeautifulSoup

def parsing (data_):
    result_ = []
    soup_ = BeautifulSoup(data_, "html.parser")
    soup_ = soup_.section.find_all('div')[2].table.form
    tmp_ = soup_.find_all('tr')

    for i_ in tmp_:
        i_ = i_.form
        col_ = i_.find_all('td')
        try:
            name = col_[0].get_text()
        except:
            name = 'NONE'
        try:
            net = col_[1].get_text()
        except:
            net = 'NONE'
        try:
            mask = col_[2].get_text()
        except:
            mask = 'NONE'
        try:
            via = col_[3].get_text()
        except:
            via = 'NONE'
        try:
            dev = col_[4].get_text()
        except:
            dev = 'NONE'
        try:
            fwmark = col_[5].get_text()
        except:
            fwmark = 'NONE'
        result_.append({"name":name, "net":net, "mask":mask, "via":via, "dev":dev, "fwmark":fwmark})

    return result_
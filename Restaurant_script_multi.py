from urllib.request import Request, urlopen;
from bs4 import BeautifulSoup as soup;
import csv;
import re;


with open('urls.csv', 'r') as ff:
    my_url = ff.readlines();
for x in range(0, 21):
    req = Request(my_url[x], headers={'User-Agent': 'Mozilla/5.0'});
    webpage = urlopen(req).read();

        
    page_soup = soup(webpage, "html.parser");
     #Find name of restaurant

    titles = page_soup.findAll("div", {"class":"FSP1Dd"});
    title = titles[0];
    Name = title.text;
    ztest = 0;
    ttest=0;
    ytest=0;

     #get url

    r_urls = page_soup.findAll("div",{"class":"NB2VS"})
    if len(r_urls) is 0:
        continue;
    else:
        r_urlss = r_urls[0].findAll('a');
        if len(r_urlss) is 2:
            r_url =  r_urlss[1]["href"];
        else:
            r_url = '-';
         
     #Find style of food & price

    styles = page_soup.findAll("div", {"class":"oTDgte"});
    style = styles[0];

    style_string = style.text;

     #Find description

    desc = page_soup.findAll("div", {"class":"DjxOn"});

    descr = desc[0];

    Description = descr.text;
     #Find google

    grat = page_soup.findAll('span', {'class':'ul7Gbc'});
    Grat = grat[0].text;

    gq = page_soup.findAll('span', {'style':'color:#777'});
    Gq = gq[0].text;
    s = re.search('(.+?) reviews', Gq);
    Gqu = s[1];

    #make div list
    sites = page_soup.findAll("div", {"class":"s"});
    l = len(sites);
    for x in range(0,l):
        if "yelp" in sites[x].text:
            if ytest is 1:
                continue;
            yelp_key = x;
            yrevs = sites[x].findAll("div",{"class":"f slp"});
            yrev = yrevs[0].text;
            Yrev = yrev.replace(u'\xa0', u' ');
            ytest=1;
        if "tripadvisor" in sites[x].text:
            ta_key = x;
            trevs = sites[x].findAll("div",{"class":"f slp"});
            if len(trevs) is 0:
                ttest = 0;
                Tr = "-";
                Tq = "-";
            else:
                trev = trevs[0].text;
                Trev = trev.replace(u'\xa0', u' ');
                ttest=1;
        if "zagat" in sites[x].text:
            zag_key=x;
            zrevs = sites[x].findAll("div",{"class":"f slp"});
            zrev = trevs[0].text;
            Zrev = zrev.replace(u'\xa0', u' ');
            ztest = 1;

    #get price
    if "$" in style_string:
        r = style_string.split("· ",1)
        Price = r[0];
        Style = r[1];
    else:
        Style = style_string;
        Price='-';



    # Yelp Extract
    if ytest is 1:
        m = re.search('Rating: (.+?) ', Yrev);
        n = re.search('- (.+?) reviews', Yrev);
        Yr = m[1];
        Yq = n[1];

    # TA Extract
    if ttest is 1:
        if "reviews" in Trev:
            o = re.search('Rating: (.+?) ', Trev);
            p = re.search('- (.+?) reviews', Trev);
            Tr = o[1];
            Tq = p[1];
        else:
            Tr = "-";
            Tq = "-";

    # Zagat Extract
    if ztest is 1:
        q = re.search('Rating: (.+?) ', Zrev);
        Zr = q[1];
    else:
        Zr = '-';

        
    with open('test_1.csv', 'a', newline='') as test_1:
        test_writer = csv.writer(test_1, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL);

        test_writer.writerow([Name, Style, Grat, Gqu, Yr, Yq, Tr, Tq, Zr, Price, '-', Description, r_url]);
        

        

            
     
     


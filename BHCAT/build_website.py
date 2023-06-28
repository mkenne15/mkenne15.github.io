################################################
# Building main table and individual object tables for sPycat using python
# Plots and figures should be in individual source folders in a jpg formats
# and have the same designation as the object in the table.
#
# Example: The object J1023+0023 should have the files
# J1023+0023.html
# J1023+0023-finder.jpg
# J1023+0023-lightcurve.jpg
# J1023+0023-paper-lightcurve.jpg
# J1023+0023-PS1.jpg
# all in the same folder. The folder and html file will be made by the
# program after the first time it's run if the folder and file don't already
# exist.
#
# Requirements: Python3, numpy, json, glob, beautifulsoup4, os, astroquery, pandas, panstamps
# Author: Mark Kennedy
#################################################


import numpy as np
import json
from glob import glob
from bs4 import BeautifulSoup as Soup
import os
import requests
from astroquery.simbad import Simbad
from astroquery.skyview import SkyView
from astropy import units as u
from astropy import constants as const
from astropy import coordinates
import pandas as pd
import aplpy
import matplotlib.pyplot as plt

def read_template_html(template_name):
    # Reads template file, formats it using Soup,
    # closes file and returns Soup object
    source = open(template_name,"r")
    template = source.read()
    soup = Soup(template,"html.parser")
    source.close()

    return soup

def add_param_col(obj_param,soup,data):
    # Adds a new column with string containing information from
    # data. If the requested data does not exists, returns "?"
    # If ID is requested, turns the input into a hyperlink

    new_col = soup.new_tag('td')

    # If doing ID column, make text hyperlink to individual target page
    if obj_param == 'ID':
        new_link = soup.new_tag('a')
        temp_name = data[obj_param]["Value"]
        new_link['href'] = "sources/" + temp_name.replace(" ", "") + "/" + temp_name.replace(" ", "") + ".html"
        new_link['target'] = "_blank"
        new_link.string = data[obj_param]["Value"]
        new_col.append(new_link)
    elif obj_param in data:
        if obj_param == 'PB':
            if data[obj_param]["Value"] == "-":
                new_col.string = str(data[obj_param]["Value"])
            else:
                Orb_P = np.around(float(data[obj_param]["Value"]), decimals=2)
                new_col.string = str(Orb_P)
                new_col['data-order'] = str(Orb_P) #For data-ordering
        else:
            new_col.string = str(data[obj_param]["Value"])
    else:
        new_col.string = "?"
    return new_col

def add_finder(name,extension,soup,style):
    # Adds a finder if it exists. If no finder exists, adds the default dss_path
    # image.
    dss_path = 'sources/' + name.replace(" ", "") + "/" + name.replace(" ", "") + "-dss.jpg"
    image_div = soup.find("div", {"id": extension})
    new_image = soup.new_tag("img")
    new_image["style"] = style + ";"
    new_image["src"] =  name.replace(" ", "") + "-dss.jpg"
    image_div.append(new_image)
    return image_div

def make_new_page(obj_data):
    # Creates a new page for the object if it does not exist,
    # or updates an already exisiting page.
    url_string = 'sources/' + obj_data['ID']["Value"].replace(" ", "")
    if not os.path.exists(url_string):
        os.makedirs(url_string)

    targ_coords_str = str(obj_data['RAJ']["Value"]) + " " + str(obj_data['DECJ']["Value"])
    targ_coords = coordinates.SkyCoord([targ_coords_str], frame="icrs", unit=(u.deg, u.deg))

    #Checking if finder exists. If not, create one and save it.
    finder_path = 'sources/' + obj_data['ID']["Value"].replace(" ", "") + "/" + obj_data['ID']["Value"].replace(" ", "") + "-dss" + ".jpg"
    if not os.path.exists(finder_path):
        dss_image = SkyView.get_images(position=targ_coords, survey=['DSS2 Red'], pixels=400)
        fig = aplpy.FITSFigure(dss_image[0])
        fig.show_circles(targ_coords.ra.value, targ_coords.dec.value, radius=0.002, facecolor='none', edgecolor='r')
        fig.show_rectangles(targ_coords.ra.value, targ_coords.dec.value, 0.083, 0.083, facecolor='b', edgecolor='b', alpha=0.1)
        fig.show_colorscale(stretch='log', cmap="Greys")
        plt.annotate('N', xy=(1.02, 1.0), xycoords='axes fraction', xytext=(1.02, 0.9), arrowprops=dict(arrowstyle="->", color='b'), horizontalalignment='center')
        plt.annotate('E', xy=(0.9, 1.02), xycoords='axes fraction', xytext=(1.02, 1.02), arrowprops=dict(arrowstyle="->", color='b'), verticalalignment='center')
        plt.title(str(obj_data['ID']["Value"]) + ", Location: " + targ_coords.to_string("hmsdms")[0])
        fig.savefig(finder_path)
        plt.clf()
        fig.close()


    # Reading individual source template
    source_soup = read_template_html("src_template.html")

    # Updating header and title to have source name
    title_tag = source_soup.find("title")
    title_tag.string = obj_data["ID"]["Value"]
    header_tag = source_soup.find("h1")
    header_tag.string = obj_data["ID"]["Value"]

    # Finding left panel and adding details from the .json file
    obj_div = source_soup.find("div", {"id": "JsonParams"})

    #Finding Table position in template
    param_table_tag = source_soup.find("tbody", {"id": "ParamTable"})

    # Adding a new row to the table for each JSON file that exists
    for i,obj_param in enumerate(obj_data):
        if (obj_param == 'ID') or (obj_param == 'COMMENTS'):
            new_div = source_soup.new_tag("div")
            new_br = source_soup.new_tag("br")
            new_div.string = str(obj_param) + ": " + str(obj_data[obj_param]["Value"])
            obj_div.append(new_div)
            obj_div.append(new_br)
        elif (obj_param == 'Apparent Mag'):
            new_row = source_soup.new_tag('tr')
            new_col = source_soup.new_tag('td')
            new_col.string = str(obj_param)
            new_col['data-order'] = str(i) #For data-ordering
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_col.string = str(obj_data[obj_param]["Value"])
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_a = source_soup.new_tag("a")
            new_a['href'] = "https://ui.adsabs.harvard.edu/#abs/" + str(obj_data[obj_param]["Ref"]) + "/abstract"
            new_a.string = str(obj_data[obj_param]["Ref"])
            new_col.append(new_a)
            new_row.append(new_col)
            param_table_tag.append(new_row)
        else:
            new_row = source_soup.new_tag('tr')
            new_col = source_soup.new_tag('td')
            new_col.string = str(obj_param)
            new_col['data-order'] = str(i) #For data-ordering
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_col.string = str(obj_data[obj_param]["Value"])
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_col.string = str(obj_data[obj_param]["Error"])
            new_row.append(new_col)
            new_col = source_soup.new_tag('td')
            new_a = source_soup.new_tag("a")
            new_a['href'] = "https://ui.adsabs.harvard.edu/#abs/" + str(obj_data[obj_param]["Ref"]) + "/abstract"
            new_a.string = str(obj_data[obj_param]["Ref"])
            new_col.append(new_a)
            new_row.append(new_col)
            param_table_tag.append(new_row)

    #Adding alternate simbad names to webpage
    simbad_div = source_soup.find("div", {"id": "SimbadNames"})
    alt_names = Simbad.query_region(targ_coords, radius=2e-4*u.deg)
    if alt_names != None:
        new_div = source_soup.new_tag("div")
        new_div.string = alt_names['MAIN_ID'][0]
        simbad_div.append(new_div)
        read_simbad_refs(alt_names['MAIN_ID'][0],source_soup)

    # Adding finder if it exists
    add_finder(obj_data['ID']["Value"],'finder',source_soup,"width:50%")

    #Adding Simbad References
    read_simbad_refs(obj_data['ID']["Value"],source_soup)

    #Updating URL string to point to HTML
    url_string = 'sources/' + obj_data['ID']["Value"].replace(" ", "") + "/" + obj_data['ID']["Value"].replace(" ", "") + ".html"
    obj_file=open(url_string,'w')
    obj_file.write(source_soup.prettify())
    obj_file.close()

def read_simbad_refs(obj_name,soup):
    ref_table = soup.find("tbody", {"id": "RefTable"})

    simbad_name = obj_name.replace("+", "%2b")
    simbad_link = "http://simbad.u-strasbg.fr/simbad/sim-id-refs?Ident= " + simbad_name
    simbad_refs = requests.get(simbad_link)
    simbad_soup = Soup(simbad_refs.text,"html.parser")


    simbad_table = simbad_soup.find("table", {"class": "sortable", "border": "2"})

    if simbad_table != None:
        simbad_rows = simbad_table.findChildren("tr")

        for i in range(1,len(simbad_rows)):
            simbad_columns = simbad_rows[i].findChildren("td")
            new_row = soup.new_tag("tr")
            new_row.append(simbad_columns[0])
            new_row.append(simbad_columns[1])
            new_row.append(simbad_columns[-2])
            new_row.append(simbad_columns[-1])
            ref_table.append(new_row)

    return ref_table



# Opening template index file, reading in HTML, and closing file again
soup = read_template_html("index_template.html")

#Finding Table position in template
table_tag = soup.find("tbody")

#Building list of json files in child directory, and sorting
#alphabetically.
json_list = glob("JSON/*")
json_list.sort()

#Building .csv file for use with TESS proposal tools (list of object RA and DEC in decimal)
ra_dec_df = pd.DataFrame(columns=('RA', 'DEC'))

# Adding a new row to the table for each JSON file that exists
for i,temp_path in enumerate(json_list):
    data = json.load(open(temp_path))
    new_row = soup.new_tag('tr')

    obj_RA = data['RAJ']["Value"]
    obj_DEC = data['DECJ']["Value"]
    coord_string = str(obj_RA) +' '+str(obj_DEC)
    obj_coords = coordinates.SkyCoord(coord_string, unit=(u.deg, u.deg))
    ra_dec_df.loc[i] = [obj_coords.ra.value,obj_coords.dec.value]

    # Here is the required fields for the table in index.html
    table_fields = ['ID','RAJ','DECJ','PB','Apparent Mag','M1']
    for field in table_fields:
      new_row.append(add_param_col(field,soup,data))

    # Adding row to table
    table_tag.append(new_row)

    # Building individual page for object
    make_new_page(data)


#Writing out new index.html file.
index_file=open("index.html",'w')
index_file.write(soup.prettify())
index_file.close()

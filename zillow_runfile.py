# Create list of search terms.
# Function zipcodes_list() creates a list of US zip codes that will be
# passed to the scraper. For example, st = zipcodes_list(['10', '11', '606'])
# will yield every US zip code that begins with '10', begins with "11", or
# begins with "606" as a single list.
# I recommend using zip codes, as they seem to be the best option for catching
# as many house listings as possible. If you want to use search terms other
# than zip codes, simply skip running zipcodes_list() function below, and add
# a line of code to manually assign values to object st, for example:
# st = ['Chicago', 'New Haven, CT', '77005', 'Jacksonville, FL']
# Keep in mind that, for each search term, the number of listings scraped is
# capped at 520, so in using a search term like "Chicago" the scraper would
# end up missing most of the results.
# Param st_items can be either a list of zipcode strings, or a single zipcode
# string.

# because Zillow's captcha to block robots,
# its more efficient to do single terms and not the full list
# Los Angeles County Zipcodes
# "90", "918", "93510", "9353", "9355"

# Orange County Zipcodes
# "926", "927", "928"

# Ventura County Zipcodes
# "91319", "91320", "930", "9062", "9063", "90680"
import time
import pandas as pd
import zillow_functions as zl
from bs4 import BeautifulSoup


# Enter zipcode term here
st_items=[]
zfile=open('z_ct.dat','r')
for z in zfile:
    z=str(z.strip())
    st_items.append(z)
st = zl.zipcodes_list(st_items[246:])
nm = str(st[0])

#print (nm)

# Initialize the webdriver.
# Use the location of the chromedriver file in your machine
# in a PC would be somethign like
#driver = zl.init_driver("C:/Users/username/chromedriver.exe")


driver = zl.init_driver("/Users/X/chromedriver")


# Go to https://www.zillow.com/homes/recently_sold
zl.navigate_to_website(driver, "https://www.zillow.com/homes/recently_sold")

# Create 10 variables from the scrapped HTML data.
# These variables will make up the final output dataframe.
df = pd.DataFrame({'address' : []
                   , 'city' : []
                   , 'state' : []
                   , 'zip' : []
                   , 'sqft' : []
                   , 'price_sqft' : []
                   , 'calculated_price' : []
                   , 'bathrooms' : []
                   , 'bedrooms' : []
                   , 'zpid' : []
                   , 'latitude' : []
                   , 'longitude' : []
                   , 'sold_date' :[]
                   , 'year_built' :[]
                   })

# Get total number of search terms.
num_search_terms = len(st)
#print (num_search_terms)
#print (st)
#exit()

# Start the scraping.
for k in range(num_search_terms):
    # Define search term (must be str object).
    search_term = st[k]

    # Enter search term and execute search.
    if zl.enter_search_term(driver, search_term):
        print("Entering search term number " + str(k+1) +
              " out of " + str(num_search_terms))
    else:
        print("Search term " + str(k+1) +
              " failed, moving onto next search term\n***")
        continue

    # Check to see if any results were returned from the search.
    # If there were none, move onto the next search.
    if zl.results_test(driver):
        print("Search " + str(search_term) +
              " returned zero results. Moving onto the next search\n***")
        continue

    # Pull the html for each page of search results. Zillow caps results at
    # 20 pages, each page can contain 26 home listings, thus the cap on home
    # listings per search is 520.
    raw_data = zl.get_html(driver)
    print(str(len(raw_data)) + " pages of listings found")
    #print (raw_data[0]) 
    #exit()

    # Take the extracted HTML and split it up by individual home listings.
    listings = zl.get_listings(raw_data)
    #listings = zl.get_listings(raw_data[0])
    #listings = listings[0] #just do the first for now to speed time exit()

    # For each home listing, extract the 11 variables that will populate that
    # specific observation within the output dataframe.
    for n in range(len(listings)):
        soup = BeautifulSoup(listings[n], "lxml")
        new_obs = []

        # List that contains number of beds, baths, and total sqft (and
        # sometimes price as well).
        card_info = zl.get_card_info(soup)

#        print ("card info", card_info)
#        badge_info = zl.get_badge_info(soup)
#        print ("badge info", badge_info)

        #print ("soup \n", soup)
        # Street Address
        new_obs.append(zl.get_street_address(soup))

        # City
        new_obs.append(zl.get_city(soup))

        # State
        new_obs.append(zl.get_state(soup))

        # Zipcode
        new_obs.append(zl.get_zipcode(soup))

        # Sqft
        sqft1 = zl.get_sqft(card_info)
        new_obs.append(sqft1)

        # get_price_sqft
        price_sqft1 = zl.get_price_sqft(card_info)
        new_obs.append(price_sqft1)

        # get_calculated_price
        new_obs.append(zl.get_calculated_price(sqft1,price_sqft1))

        # Bathrooms
        new_obs.append(zl.get_bathrooms(card_info))

        # Bedrooms
        new_obs.append(zl.get_bedrooms(card_info))

        # zpid for each property
        new_obs.append(zl.get_zpid(soup))

        # Latitude
        new_obs.append(zl.get_latitude(soup))

        # Longitude
        new_obs.append(zl.get_longitude(soup))
        # sale date
        new_obs.append(zl.get_sold_date(soup))
        new_obs.append(zl.get_yBuilt(soup))

        # Append new_obs to df as a new observation
        if len(new_obs) == len(df.columns):
            df.loc[len(df.index)] = new_obs

# Close the webdriver connection.
zl.close_connection(driver)

# Write df to CSV.
dt = time.strftime("%Y-%m-%d") + "_" + time.strftime("%H%M%S")
file_name = nm + "-" + str(dt) + ".csv"
df.to_csv(file_name, index = False,  header=['address', 'city', 'state', 'zip', 'sqft',  'price_sqft', 'total_price', 'bathrooms', 'bedrooms', 'zpid', 'latitude', 'longitude', 'sale_date', 'year_Built'])

import requests
import random
import time
import json

def float_range(start, stop=None, step=None):
    if stop == None:
        stop = start + 0.0
        start = 0.0
    if step == None:
        step = 1.0
    while start < stop:
        yield start
        start += step


max_north = 42.0254
min_south = 41.6417
min_west = -87.8617
max_east = -87.608

unit_delta_y = 0.02
unit_delta_x = 0.04
num_retries = 5

listings = []
ids = []
url = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState={"pagination":{currentPage: %s},"mapBounds":{"west":%s,"east":%s,"south":%s,"north":%s},"isMapVisible":true,"mapZoom":14,"filterState":{"isPreMarketForeclosure":{"value":false},"isPreMarketPreForeclosure":{"value":false},"isMakeMeMove":{"value":false}},"isListVisible":true}'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'}
iters = ((max_north - min_south) / unit_delta_y) * ((max_east - min_west) / unit_delta_x) * 20
count = 0
with open('results.json', 'w') as f:
    for lon in float_range(min_south, max_north, unit_delta_y):
        south = lon - (unit_delta_y * 0.1)
        north = lon + unit_delta_y

        for lat in float_range(min_west, max_east, unit_delta_x):
            west = lat - (unit_delta_x * 0.1)
            east = lat + unit_delta_x

            for current_page in range(1, 21):
                print(f'\n{(count / iters):.4%} done')
                print(f'Page {current_page} \nNorth {north} \nSouth {south} \nEast {east}\nWest {west}')
                
                data = None
                for i in range(num_retries):
                    try:
                        data = requests.get(url % (current_page, west, east, south, north), headers=headers).json()
                        break
                    except:
                        print(f'retry count {i}')
                        if i == num_retries - 1:
                            raise
                        else:
                            continue
                if 'pagination' in data['queryState'] and data['queryState']['pagination']['currentPage'] != current_page:
                    break
                
                results = data['searchResults']['listResults']
                print(f'Found {len(results)} records')
                filtered = [result for result in results if result['id'] not in ids]
                print(f'Found {len(filtered)} new records')
                
                new_ids = [result['id'] for result in filtered]
                listings.extend(filtered)
                ids.extend(new_ids)
                time.sleep(random.random() * random.randrange(1, 5))
                count += 1
    json.dump(listings, f, indent=2)

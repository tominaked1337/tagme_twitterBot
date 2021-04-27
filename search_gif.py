import requests
import json
import os

def get_gif(search_term):
    # set the apikey and limit
    apikey = "LIVDSRZULELA"  # test value
    limit = 1

    # set the query
    response = requests.get(
        "https://g.tenor.com/v1/search?q=%s&key=%s&limit=%s" % (search_term, apikey, limit))

    if response.status_code == 200:
        # load gif content
        gif = json.loads(response.content)
    else:
        gif = None

    # set the gif destination URL
    gif_url = gif['results'][0]['media'][0]['mediumgif']['url']

    # create a gif file from the source
    r = requests.get(gif_url, allow_redirects=True)

    open('sgif.gif', 'wb').write(r.content)

    # will just return the gif name to be opened when the mention appear

    return 'sgif.gif'

def remove_gif():
    # get the current working path and delete all the '.gif' files in the directory
    dir_name = os.path.dirname(os.path.abspath(__file__))
    files_list = os.listdir(dir_name)

    for item in files_list:
        if item.endswith(".gif"):
            os.remove(os.path.join(dir_name, item))







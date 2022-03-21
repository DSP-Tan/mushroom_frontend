import wikipedia
import requests
import json
from PIL import Image

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

url='https://en.wikipedia.org/w/api.php'

def get_wiki_image(search_term):
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return 0


def Wiki_Api(mushroom_name):

    mushroom_dict = {}

    params={
    'action':'query',
    'format':'json',
    'titles':mushroom_name,
    'prop':'revisions',
    'rvsection':0,
    'rvprop':'content'}

    #Inital response from Wiki web page
    response=requests.get(url,params).json()

    #Find key for Json
    key = list(response['query']['pages'].keys())[0]
    lines = response['query']['pages'][key]['revisions'][0]['*'].split('\n')
    cap_counter  =0
    for line in lines:
        if 'howEdible' in line:
            mushroom_dict["howEdible"] = line.split('=')[1].strip(" ").strip("}")
        #if 'howEdible2' in line:
        #   mushroom_dict["howEdible2"] = line.split('=')[1].strip(" ")
        if 'whichGills' in line:
            mushroom_dict["whichGills"] = line.split('=')[1].strip(" ")
        if 'capShape' in line and cap_counter==0:
            mushroom_dict["capShape"] = line.split('=')[1].strip(" ")
            cap_counter += 1
        # if 'hymeniumType' in line:
            #   mushroom_dict["hymeniumType"] = line.split('=')[1].strip(" ")
            # if 'stipeCharacter' in line:
        #   mushroom_dict["stipeCharacter"] = line.split('=')[1].strip(" ")
        # if 'ecologicalType' in line:
        #   mushroom_dict["ecologicalType"] = line.split('=')[1].strip(" ")
        # if 'sporePrintColor'  in line:
        #   mushroom_dict["sporePrintColor"] = line.split('=')[1].strip(" ")

    return (mushroom_dict)


def pic_to_dict(dic_item):
    full_loc = f"Wiki_images/{dic_item}.jpeg"
    im = Image.open(full_loc)
    size = 126,126
    im.thumbnail(size)
    return full_loc

def convert_name(name):
    return name.replace('_'," ").capitalize()



# To Do: Do not exclude other.
def get_max_mush(dict_res,other=True, weights=[1,1,1]):
    '''
    This will return the dicionary item of the species
    with the highest score. If other is set to True this
    includes the 'Other' species, if it is set to false
    the other is not included.

    The weights have to be set to the accuracy/or some metric
    of each model, so that later on you do not take as the maximum
    score a high score from a bad model.

    The weights only come into play after you first find the maximum,
    so the implementation is not as straight forward as it seems. You
    could just have an option where the weights are only applied when
    a certain flag is given. Anyway, for now we do not have the weights
    and so we will continue without them but with this reminder.
    '''
    max_prob=0
    for key, value in dict_res.items():
        if key=='Other':
            continue
        if value > max_prob:
            max_res=(key,value)
            max_prob=value
    return max_res


# store results in a list of dicts.
def query_species(payload,base_url):

    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    results=[]
    maxes=[]
    for i in [1, 2, 3]:
        url=base_url+str(i)
        predict=requests.post(url , headers = headers , data = payload).json()
        # Prediction is output as str, eval returns it to dict.
        result=eval(predict)
        max_mush=get_max_mush(result)
        maxes.append(max_mush)
        print(f"\n\nThe out put of model {i} is :\n{result}\nThe most likely mushroom is :\n{max_mush}")
        results.append(result)
    maxes_dict={i[0]:i[1] for i in maxes}
    print(f"\n\nHere are the maxes in dictionary form\n{maxes_dict}")
    ultimate_mush=get_max_mush(maxes_dict,other=False)
    print(f"The final chosen mushroom is:\n{ultimate_mush}")
    return ultimate_mush



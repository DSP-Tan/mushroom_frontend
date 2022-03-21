
import streamlit as st

import requests
import os
import io
import base64
import json
import random
from PIL import Image
from utils import Wiki_Api, get_wiki_image, pic_to_dict, convert_name
from utils import get_max_mush, query_species



st.set_page_config(
        page_title="Mushroom Magic", # => Quick reference - Streamlit
        page_icon="🍄",
        layout="centered", # wide
        initial_sidebar_state="auto") # collapsed

st.markdown("<h1 style='text-align: center; color: black;'>Mushroom Magic 🍄</h1>", unsafe_allow_html=True)



spinner_quotes = ['“All Fungi are edible. Some fungi are only edible once.” ― Polish/Croatian proverb',
                  '“Nature alone is antique, and the oldest art a mushroom.” ~ Thomas Carlyle',
                  'A meal without mushrooms is like a day without rain. - John Cage',
                  'Advice is like mushrooms. The wrong kind can prove fatal. - Charles E. McKenzie',
                  'It\'s interesting, isn\'t it? . . . the chandelier . . . it reminds me of mushroom soup. — Tennessee Williams',
                  'Why did the mushroom go to the party? Because he\'s a fungi! — Louis Tomlinson',
                  'Look around when you have got your first mushroom or made your first discovery: they grow in clusters. — George Polya',
                  'From dead plant matter to nematodes to bacteria, never underestimate the cleverness of mushrooms to find new food! — Paul Stamets',
                  'Compliments are like mushrooms, the most beautiful are the most poisonous. - Italian proverb',
                  "One who is noisy in the wood, scares away mushrooms. - Russian proverb"
                  ]

# Lot's of nice proverbs here: https://quoteproverbs.com/mushrooms/


#st.image(get_wiki_image('Russula nobilis')) # returning the Wikipedia image
label = 'Upload your Mushroom here. (refresh/retry if error)'

image = st.file_uploader(label, type=None, accept_multiple_files=False, key=None, help=None, on_change=None)

# Convert image to format suitable for API call, and make API call.
if(image):
    im_PIL = Image.open(image)

    img_path="temp.jpg"
    im_PIL.save(img_path)
    #im_PIL.save("../"+img_path)
    # Temporary work around to ensure streamlit runs correctly whether it is run in
    # The app folder or in the mushroom learning base.

    # Set up image Jerome's way.
    with open(img_path, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    payload = json.dumps({"image": im_b64})




    size= 256,256
    cols = st.columns(3)
    if cols[1].button('Identify your Mushroom'):


        random_num = random.randint(0,len(spinner_quotes)-1)
        with st.spinner(spinner_quotes[random_num]):
            predict_cols = st.columns(3)

            with predict_cols[0]:
                st.header("Upload")

                im= Image.open(image)
                im.thumbnail(size)
                st.image(im)

            # Call API using requests to run prediction.
            url="https://mushroom-docker-lpuaioudtq-ew.a.run.app/species"
            ultimate_mush= query_species(payload,url)
            preidction = convert_name(ultimate_mush[0])
            certainty  = ultimate_mush[1]

            with predict_cols[1]:

                st.header("Prediction:")
                st.info(preidction)

                # st.metric(label="Certainty",value=f'{int(100*certainty)}%')
                st.markdown("<h3 style='text-align: center; color: black;'>Certainty: <br> "+ str(int(100*certainty))+"%</h3>", unsafe_allow_html=True)

            with predict_cols[2]:
                st.header("Wiki Image")
                st.image(get_wiki_image(preidction))

            expander_cols = st.columns(3)

            try:
                if not Wiki_Api(preidction)["capShape"]:
                    pass

                else:
                    print("We have the else branch")
                    with expander_cols[0]:
                        expander_info = expander_cols[0].expander("Cap Shape:")
                        im3= Image.open(pic_to_dict(Wiki_Api(preidction)["capShape"]))
                        im3.thumbnail(size)
                        expander_info.image(im3)
                    with expander_cols[1]:
                        expander_hydro = expander_cols[1].expander("Hymenium Shape:")
                        im4= Image.open(pic_to_dict(Wiki_Api(preidction)["whichGills"]))
                        im4.thumbnail(size)
                        expander_hydro.image(im4)
                    with expander_cols[2]:
                        expander_ed = expander_cols[2].expander("Edible:")
                        im5= Image.open(pic_to_dict(Wiki_Api(preidction)["howEdible"]))
                        im5.thumbnail(size)
                        expander_ed.image(im5)


                        # expander_interesting = st.expander('interesing info')
                        # expander_interesting.write('''A. muscaria was used by both shamans and laypeople alike, and was used recreationally as well as religiously. In eastern Siberia,
                        #                            the shaman would take the mushrooms, and others would drink his urine. This urine, still containing psychoactive elements,
                        #                            may be more potent than the A. muscaria mushrooms with fewer
                        #                            negative effects such as sweating and twitching, suggesting that the initial user may act as a screening
                        #                            filter for other components in the mushroom.''')
            except:
                pass
                st.markdown('#')
                st.markdown("<p style='text-align: justify; color: black; font-size:8px;'>Disclaimer: \n Don\'t consume any mushroom unless you are 100% certain that it is edible. \
                         The Mushroom magic app cannot provide this certainty. \n\
                         The Mushroom magic app is published as a student project, \
                         but WITHOUT ANY WARRANTY; without even the implied warranty of \
                         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. \
                         </p>", unsafe_allow_html=True)

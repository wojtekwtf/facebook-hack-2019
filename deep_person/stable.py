# XXX: INSPIRATION =====================================
# https://gist.github.com/giuseppebonaccorso/061fca8d0dfc6873619efd8f364bfe89
# https://github.com/yu4u/convnet-drawer
# https://www.tensorflow.org/alpha/tutorials/sequences/word_embeddings
# music: https://www.youtube.com/watch?v=-gXrS6eKfjk

# XXX: DATASETS ========================================
# https://data.world/datasets/jobs
# https://data.world/wnedds/jobs-by-likelihood-of-automation

# ======================================================

#######################
# F1 [SCORES] | [REF] #
# cCON: 0.50  | 0.37  #
# cOPN: 0.36  | 0.38  #
# cEXT: 0.50  | 0.39  #
# cNEU: 0.50  | 0.35  #
# cAGR: 0.46  | 0.39  #
#######################

# XXX: WE BEAT THIS PAPER!!! ===========================
# https://www.researchgate.net/figure/Detection-model-of-waring-scenario-for-possible-cases-of-blue-feeling_fig1_320875235
# ======================================================

# FIXME: (cambridge analytica like project)
# (0) XXX: check what (s)EXT prefix does
# (1) add more sentiment analysis to TEXT (not only personality)
# (2) [done?] improve speed --> one load/extension
# (3) what about profile analysis --> likes/favorites/photo?
#       some parameters like height/hair color/age analysis

# FIXME: better datasets?
# https://web.archive.org/web/20180428085315/http://mypersonality.org/wiki/doku.php?id=download_databases
# linkedin profiles: https://www.kaggle.com/killbot/linkedin/version/1
# https://www.kaggle.com/datasets

# FIXME: todolist?
# (1) twitter API
# (2) scrapping tweets for user
# (3) analyzing tweets
# (4) final analysis
# (6) more parameters (from nltk, textlib)
# (5) repair/add dataset
#      essays
#      20 -> 30
#      and framing sentences
#      stats for dataset
#      new parameters before???
# +(6) jobs? automation dataset
# +(7) tutorial scrapper?
# +(8) dataset with job:profile -> which category?
#                       let say 20 jobs
# +(9) building habits? / or something

import session

from glob import glob

from model import str2vec
from model import DeepPersonality
from model import model_deep_personality
from data  import get_vec4tok, dataset_mypersonality

COLUMNS = ["cEXT", "cNEU", "cAGR", "cCON", "cOPN"]

def get_model_name(trait:str):
    return model_deep_personality+"_"+trait

def load_our_cache():
    dataset = dataset_mypersonality()
    cached_vec,_ = get_vec4tok(dataset)
    for trait in COLUMNS:
        print("[\033[92m{}\033[0m]".format(trait))
        if glob(get_model_name(trait)+"*") != []:
            print("[DEEP_PERSONALITY] loading weights")
            cached_models[trait] = DeepPersonality()
            cached_models[trait].load_weights(get_model_name(trait))
    return True, cached_models, cached_vec

cached = False # can be manually triggered
cached_models = {}; cached_vec = object
def predict_for_our_models(TEXT):
    global cached, cached_models, cached_vec
    if not cached:
        cached, cached_models, cached_vec = load_our_cache()
    X_input = str2vec(cached_vec, TEXT); result = {}
    for trait in COLUMNS: # for every model
        result[trait] = cached_models[trait].predict(X_input)
    return result

"""
FIXME: benchmarking
from tqdm import tqdm
for _ in tqdm(range(0, 1000)):
    predict_for_our_models(TEXT)
"""

from pprint import pprint

######################
def sentence_split(text:str, max_length:int=20):
    lsent = []; lex = text.split(); max_length = int(max_length*0.75)
    for i in range(0, len(lex), int(max_length/2)):
        lsent.append(" ".join(lex[i:min(i+max_length, len(lex))]))
    return lsent

def sentence_mean(lsent:list):
    darr = {"cEXT":0.5, "cNEU":0.5, "cAGR":0.5, "cCON":0.5, "cOPN":0.5}
    for s in lsent:
        res = predict_for_our_models(s)
        for key in res.keys():
            darr[key] = (darr[key]+res[key])/2
    return darr

arr = sentence_split("""Hi! I am very happy and nervus. I don't like people. I hate
        racism. And I don't know basicly how to talk to people. How to feel
        their feelings""")
print(arr)
res = sentence_mean(arr)
print(res)

######################

TEXT_1 = "Hi! I am very happy! What do you think? Is it good?"
pprint(predict_for_our_models(TEXT_1))

TEXT_2 = "I don't like going outside, it's boring in general."
pprint(predict_for_our_models(TEXT_2))

# FIXME: something wrong with tagging?
"""
   @1  @2
EXT p  l
NEU l  l
AGR p  p
CON l  l
OPN p  p
"""

# from paper
"""
•	 Extroversion (EXT). Is the person outgoing, talkative, and energetic versus reserved and solitary?
•	 Neuroticism (NEU). Is the person sensitive and
nervous versus secure and confi dent?
•	 Agreeableness (AGR). Is the person trustworthy,
straightforward, generous, and modest versus
unreliable, complicated, meager, and boastful?
•	 Conscientiousness (CON). Is the person effi -
cient and organized versus sloppy and careless?
•	 Openness (OPN). Is the person inventive and curious versus dogmatic and cautious?
"""

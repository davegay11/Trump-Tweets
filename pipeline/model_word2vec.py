import pandas as pd
import numpy as np
# Initialize and train the model (this will take some time)
from gensim.models import word2vec
# Import the built-in logging module and configure it so that Word2Vec 
# creates nice output messages
import logging

def create_model(
        clean_data_path,
        save_path, 
        num_features=300, 
        min_word_count=10, 
        num_workers=4, 
        context=10, 
        downsampling=1e-3,
        logging=True):
    ''' 
    Create a word2vec model for a certain person in the corpus. Given that there aren't many 
    tweets for anybody besides Trump it may be a bit difficult to use this model as a 
    comparison in any meaningful way
    '''

    df = pd.read_csv(clean_data_path, header=0)

    if logging:
        logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',    level=logging.INFO)

    print "Training model..."
    model = word2vec.Word2Vec(
            [str(s).split() for s in list(df['clean_text'])], 
            workers=num_workers, size=num_features, \
            min_count = min_word_count, \
            window = context, sample = downsampling)

    # calling init_sims make the training more efficient if we don't plan on
    # training the model any further
    model.init_sims(replace=True)

    # It can be helpful to create a meaningful model name and 
    # save the model for later use. You can load it later using Word2Vec.load()
    model.save(save_path)
    return model

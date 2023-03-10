'''
This portion consists of making GMM model.

Different Phase Strategy to be adopted:

1. First Phase:
    a. Just focus on developing the model.
    b. Weather it be full of accuracy or not. Dont't think of accuracy at first
    c. Use GMM with any parameters.

2. Second Phase
    a. Try to optimize the model's hyper-parameter
    b. Focus only on hyper-parameters

3. Third Phase:
    a. Try to build the functionality of data pre-processing
    b. Add extra functionality


Currently practicing on phase1. Timeline 1 day.
'''

'''
Tips: If the model representive of the different audio files are to be made.
      Just stack the feature of the different audio files into one array
      and find out the gaussian distribution for the model. 
'''

import os
import pickle
import joblib
from sklearn.mixture import GaussianMixture
from SpeakerRecognition.ExtractMFCCFeature import ExtractFeature
import numpy as np
# this is just a pycharm error
#from Filename import Classname



# Documentation at: https://scikit-learn.org/stable/modules/generated/sklearn.mixture.GaussianMixture.html
# Description of the functional parameters
# these functional parameters needs to be tuned.

# gmm = GMM(n_components=16, n_iter=200, covariance_type='diag', n_init=3)



def makeModel(pipelined_data_frame, model_save_path):
    # model_save_path = "speakers_model/" #directory in which model is to saved
    # checking if the directory exist - MT 
    if not os.path.isdir(model_save_path):
    # if the directory is not present then create it.
        os.makedirs(model_save_path)
    # end - MT

    ef = ExtractFeature #object to extract the feature
    stacked_feature = np.asarray(())

    first_audio_location_in_frame = pipelined_data_frame["audio_path"].iloc[0] #first audio path in pandas frame
    stacked_feature = ef.extract_features(first_audio_location_in_frame) #first training audio's feature

    for index, row in pipelined_data_frame.iterrows(): #iterating through the pandas frame

        # find the number of voice file such as '2' in 'dataset/train/antora/2.wav' - MT
        model_name = pipelined_data_frame["target_speaker"][index]  # name of model represent's whose voice model??
        saved_speech_number = pipelined_data_frame['audio_path'][index].split('.')[0][-1] 

        if index != 0: #escaping the first audio's feature
            ef = ExtractFeature  # object for extracting the MFCC feature
            currently_fetched_feature = ef.extract_features(row['audio_path']) # one feature extracted
            stacked_feature = np.vstack((stacked_feature, currently_fetched_feature)) #stacking the features

    



            # model_name = pipelined_data_frame["target_speaker"].iloc[0]+".gmm"  # name of model represent's whose voice model??

            gmm = GaussianMixture(n_components=16, covariance_type='diag', max_iter=500, n_init=3, verbose=1)
            gmm.fit(stacked_feature) #generating the GMM model of the stacked features
            saved_model = model_save_path + model_name + saved_speech_number +".gmm"
            print(saved_model)
            joblib.dump(gmm, saved_model)
            # pickle.dump(gmm, open(model_save_path + model_name + saved_speech_number, 'wb'))

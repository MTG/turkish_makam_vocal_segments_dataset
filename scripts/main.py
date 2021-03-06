'''
Created on Oct 7, 2016

@author: georgid
'''
# import sys
from intersect_vocal_and_pitch import     generate_vocal_segments
import numpy as np
from get_vocal_recordings import intersect_vocal_sarki_symbTr,\
    get_recIDs_OK_vor_vocal
import os
from intersect_vocal_and_pitch import fetch_voiced_sections
import logging
from mir_eval.io import load_delimited, load_intervals
import json
VOCAL_SECTIONS_ANNOTATION_EXT = '.vocal_sections_anno'
VOCAL_ACTIVITY_EXT = '.vocal_anno'
VOCAL_ONSETS_ANNO = '.vocal_onsets_anno'

logging.basicConfig(level=logging.DEBUG)


def load_onset_anno_recs(): 
    '''
    # rec IDs of sarkis with annotated vocal note onsets
    '''
    import csv
    recIDs_onsets = []
    with open('/home/georgid/Downloads/list_sarkis.csv', 'r') as f:
        
        reader = csv.reader(f)
        for row in reader:
            recIDs_onsets.append(row[0])
    return recIDs_onsets


def generate_voiced_sections(musicbrainzid, output_dir):
    
    #### 1. voiced intervals
    voiced_intervals = fetch_voiced_sections(musicbrainzid)
     
    #### store vocal_intervals in tab separated file
    file_name = os.path.join(output_dir, musicbrainzid + VOCAL_SECTIONS_ANNOTATION_EXT)
    if os.path.exists(file_name):
        raw_input('file {} exists. Are you sure you want to overwrite it with automatically extracted onsets? if Yes, press enter'.format(file_name))
    f = open(file_name, 'w')
    for srat_time,end_time in voiced_intervals:
        f.write('{}\t{}\n'.format(srat_time,end_time))
    logging.warning('written file {}'.format(file_name))    


def generate_voiced_pitch_contours(musicbrainzid, output_dir):
    #### 1. voiced intervals
#     file_name = os.path.join(output_dir, musicbrainzid + VOCAL_SECTIONS_ANNOTATION_EXT)
    file_name = os.path.join(output_dir + '/' + musicbrainzid, musicbrainzid + VOCAL_ACTIVITY_EXT)

    voiced_intervals = load_voiced_segments(file_name)
            
#     ###### 2.  generate vocal pitch annotation
    intersected_pitch_series = generate_vocal_segments(musicbrainzid, voiced_intervals, for_pitch=True)
    if intersected_pitch_series == None:
            logging.warning('no vocal pitch contour in {}'.format(musicbrainzid))
    else:
            store_pitch_anno(musicbrainzid, intersected_pitch_series,  output_dir)
    
     #     ### plot intersected_pitch_series
#     import matplotlib.pyplot as plt
#     
#     pitch_array = np.array(intersected_pitch_series)
#     plt.plot(pitch_array[:,0], pitch_array[:,1])
#     plt.show()


   

def generate_voiced_notes(musicbrainzid, output_dir):
    #### 1. voiced intervals
#     file_name = os.path.join(output_dir, musicbrainzid + VOCAL_SECTIONS_ANNOTATION_EXT)
    file_name = os.path.join(output_dir, musicbrainzid + VOCAL_ACTIVITY_EXT)
    voiced_intervals = load_voiced_segments(file_name)
    
    ###### 3. generate vocal onset annotations
    vocal_notes, onsets_ts_URI = generate_vocal_segments(musicbrainzid, voiced_intervals, for_pitch=False)
    if vocal_notes == None or len(vocal_notes) == 0:
            logging.warning('no vocal onsets  in {}'.format(musicbrainzid))
    
    import csv
    URI_vocal_onsets = onsets_ts_URI[:-4] + '_vocal.txt' # aligned_notes_vocal
    with open(URI_vocal_onsets,'w') as f:
              writer = csv.writer(f, delimiter='\t')
              writer.writerows(vocal_notes)
    print 'written file + ' +  URI_vocal_onsets
#     store_time_anno(musicbrainzid, vocal_notes, output_dir)
    
    
    


def load_voiced_segments(file_name):
    '''
    convenience function
    '''
    try:
        voiced_intervals = load_intervals(file_name)
    except:
        starts, values, durations = load_delimited(file_name, [float, float, float])
        # Stack into an interval matrix
        starts = np.array(starts)
        durations = np.array(durations)
        voiced_intervals = np.array([starts, starts + durations]).T # assume a middle column present, this happens on expoert of regions layer in SV
    return voiced_intervals


def store_pitch_anno(musicbrainzid, intersected_pitch_series, pitch_dir):
    '''
    store intersected vocal pitch contour in a given dir pitch_dir
    output format tuple: time,pitch 
    '''
    
    pitch_array = np.array(intersected_pitch_series) 
    if not os.path.exists(pitch_dir):
        os.mkdir(pitch_dir)
    file_name = os.path.join(pitch_dir, musicbrainzid + '.pv')
    f = open(file_name, 'w')
    for time,pitch in pitch_array[:,0:2]:
        f.write('{},{}\n'.format(time,pitch))
    logging.warning('written file {}'.format(file_name))

def store_time_anno(musicbrainzid, timestamps, output_dir):
    # store vocal onset annotation
    if timestamps == None:
            return
    file_name = os.path.join(output_dir, musicbrainzid + VOCAL_ONSETS_ANNO)
    f = open(file_name, 'w')
    for ts in timestamps:
        f.write('{}\n'.format(ts) )
    logging.warning('written file {}'.format(file_name))


    

if __name__ == '__main__': # intersect 
    
#     rec_ID = 'ba1dc923-9b0e-4b6b-a306-346bd5438d35'
#     pitch_output_dir = sys.argv[1]
    logging.basicConfig(level=logging.DEBUG)
    
    ############### with annotated note onsets
    data_dir = '/Users/joro/Documents/Phd/UPF/voxforge/myScripts/turkish_makam_vocal_segments_dataset/data/' 
    
    # take from list https://docs.google.com/spreadsheets/d/1f9wyxB6emGHvVGUhIjNQwSxxhOJhPAdNzA2BieyKVXw/edit?usp=sharing
    list_vocal_sarkis_onset_detected =[
#     'dfc16e22-0aae-4bd0-a32c-5c000130e96a',
#     '8a0260ac-e8a5-42ed-af2a-a6f547996281',
#     'f5ddf3aa-643b-4655-a9b7-3736e9a4d3d3',
#     'f5a89c06-d9bc-4425-a8e6-0f44f7c108ef',
#     '727cff89-392f-4d15-926d-63b2697d7f3f',
#     'b49c633c-5059-4658-a6e0-9f84a1ffb08b',
#     '567b6a3c-0f08-42f8-b844-e9affdc9d215',
#     'feda89e3-a50d-4ff8-87d4-c1e531cc1233',
#     'eaea7f6b-fb94-4982-9ac7-162f1503182a',
#     '6d892b77-9733-4ba7-a497-646c969c72b8',
#     '8c7eccf5-0d9e-4f33-89f0-87e95b7da970',
#     '0b45417b-acb4-4f8a-b180-5ad45be889af',
#     '6d97f1f8-5f05-4c5c-b1ab-2757fdc3e746',
#     '9c26ff74-8541-4282-8a6e-5ba9aa5cc8a1', 
#     '2ec806b4-7df2-4fd4-9752-140a0bcc9730',
#     '92ef6776-09fa-41be-8661-025f9b33be4f',
    'c7a31756-a7d5-4882-bdf7-9c6b23493597'
    ]
   

    for recID in list_vocal_sarkis_onset_detected:
        output_dir = data_dir + recID + '/' 
        generate_voiced_sections(recID, output_dir)
#         generate_voiced_notes(recID, output_dir)





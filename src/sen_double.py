import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import math

input_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/sandbox/input.txt'
output_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/sandbox/output.txt'

mapping_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/dictionary/pinyin_hanzi.txt'
double_json_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/json/double_sen.json'

def get_mapping():
    mapping = {}
    mapping_handler = open(mapping_file_path, 'r')
    raw_mapping_str_list = mapping_handler.readlines()

    # Add the mapping relations
    for raw_str in raw_mapping_str_list:
        raw_list = raw_str.split(' ')
        raw_list[-1] = raw_list[-1].replace('\n', '')
        mapping[raw_list[0]] = raw_list[1: ]
    
    return mapping

def get_weight_dict():
    json_handle = open(double_json_path, 'r')
    return json.loads(json_handle.readlines()[0].replace('\'', '\"'))

def try_match(pinyin_list, start, weight_dict, mapping):
    available_len = min(4, len(pinyin_list) - start)
    legal_hanzi_mat = [mapping.get(pinyin_list[start + i], []) for i in range(available_len)]
    legal_phrases = []

    # Try phrases of 2 characters
    if available_len > 1:
        for i in legal_hanzi_mat[0]:
            for j in legal_hanzi_mat[1]:
                if i + j in weight_dict:
                    legal_phrases.append(i + j)
        if len(legal_phrases):
            return (2, legal_phrases)
    
    # Try phrases of 4 characters
    if available_len > 3:
        for i in legal_hanzi_mat[0]:
            for j in legal_hanzi_mat[1]:
                for k in legal_hanzi_mat[2]:
                    for l in legal_hanzi_mat[3]:
                        if i + j + k + l in weight_dict:
                            legal_phrases.append(i + j + k + l)
        if len(legal_phrases):
            return (4, legal_phrases)
    
    # Try phrases of 1 character
    if available_len > 0:
        for i in legal_hanzi_mat[0]:
            if i in weight_dict:
                legal_phrases.append(i)
        if len(legal_phrases):
            return (1, legal_phrases)

    # Try phrases of 3 characters
    if available_len > 2:
        for i in legal_hanzi_mat[0]:
            for j in legal_hanzi_mat[1]:
                for k in legal_hanzi_mat[2]:
                    if i + j + k in weight_dict:
                        legal_phrases(i + j + k)
        if len(legal_phrases):
            return (3, legal_phrases)
    
    # No match
    return (0, [])

def main():
    input_handler = open(input_file_path, 'r')
    output_handler = open(output_file_path, 'w')

    # Load the map from pinyin to hanzi
    mapping = get_mapping()
    mapping['^'] = ['^']

    # Load the dict of weights
    weight_dict = get_weight_dict()

    # Get the hanzi str from pinyin
    for pinyin_str in input_handler.readlines():

        # Start the pinyin str with a ^, end the pinyin str with a $
        pinyin_list = ['^']
        pinyin_list += pinyin_str.split(' ')
        pinyin_list[-1] = pinyin_list[-1].replace('\n', '')
        pinyin_list.append('$')
        
        # Start the DP with empty list
        # The tuple: (path_len, prefix)
        dp_list = []
        dp_list.append([[0, '^']])

        flag = 1
        # Store the previous/now legal phrases for DP
        prev_legal_phrases = ['^']
        now_legal_phrases = []

        while flag < len(pinyin_list):

            # Get the legal phrases & forward the pointer
            phrase_len, now_legal_phrases = try_match(pinyin_list, flag, weight_dict, mapping)
            flag += phrase_len

            # If there are no legal phrases, break
            if not len(now_legal_phrases):
                break

            # Set up the new layer of DP
            new_layer_in_dp = [[math.inf, ''] for _ in range(len(now_legal_phrases))]

            for ind_in_prev, prev_phrase in enumerate(prev_legal_phrases):
                for ind_in_now, now_phrase in enumerate(now_legal_phrases):

                    # Get the weights dict of doubles started by the prev_phrase
                    weights = weight_dict.get(prev_phrase, None)
                    if weights == None:
                        continue

                    # Get the counts and the len of the path
                    tuple_count = weights.get(prev_phrase + now_phrase, 0)
                    tot_count = weights['total']
                    path_len = -math.log(tuple_count / tot_count) if tuple_count != 0 else math.inf
                    path_len += dp_list[-1][ind_in_prev][0]

                    # Update the new layer of DP
                    if path_len <= new_layer_in_dp[ind_in_now][0]:
                        new_layer_in_dp[ind_in_now][0] = path_len
                        new_layer_in_dp[ind_in_now][1] = dp_list[-1][ind_in_prev][1] + now_phrase
            
            # Push the new layer to DP list
            dp_list.append(new_layer_in_dp)
            print(dp_list)

            # Update the prev_legal_phrases
            prev_legal_phrases = now_legal_phrases
        
        print(dp_list[-1])

if __name__ == '__main__':
    main()
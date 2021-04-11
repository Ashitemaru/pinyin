import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import math

input_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/test/input.txt'
output_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/test/output.txt'

mapping_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/dictionary/pinyin_hanzi.txt'
double_json_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/assets/json/triple.json'

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

def main():
    input_handler = open(input_file_path, 'r')
    output_handler = open(output_file_path, 'w')

    # Load the map from pinyin to hanzi
    mapping = get_mapping()
    mapping['^'] = ['^']
    mapping['$'] = ['$']

    # Load the dict of weights
    weight_dict = get_weight_dict()

    # Get the hanzi str from pinyin
    for pinyin_str in input_handler.readlines():

        # Start the pinyin str with a ^, end the pinyin str with a $
        pinyin_list = ['^', '^']
        pinyin_list += pinyin_str.split(' ')
        pinyin_list[-1] = pinyin_list[-1].replace('\n', '')
        pinyin_list += ['$', '$']
        
        # Start the DP with empty list
        # The tuple: (path_len, prefix)
        dp_list = [[[0, '^']], [[0, '^']]]

        flag = 2
        while flag < len(pinyin_list):

            # Get the legal hanzi & forward the pointer
            pprev_legal_hanzi = mapping[pinyin_list[flag - 2]]
            prev_legal_hanzi = mapping[pinyin_list[flag - 1]]
            now_legal_hanzi = mapping[pinyin_list[flag]]
            flag += 1

            # If there are no legal hanzi, break
            if not len(now_legal_hanzi):
                break

            # Set up the new layer of DP
            new_layer_in_dp = [[math.inf, ''] for _ in range(len(now_legal_hanzi))]

            for ind_in_now, now_hanzi in enumerate(now_legal_hanzi):
                for ind_in_pprev, pprev_hanzi in enumerate(pprev_legal_hanzi):
                    for ind_in_prev, prev_hanzi in enumerate(prev_legal_hanzi):

                        # Get the weights dict of doubles started by the prev_hanzi
                        weights = weight_dict.get(pprev_hanzi + prev_hanzi, None)
                        if weights == None:
                            continue

                        # Get the counts and the len of the path
                        tuple_count = weights.get(pprev_hanzi + prev_hanzi + now_hanzi, 0)
                        tot_count = weights['total']
                        path_len = -math.log(tuple_count / tot_count) if tuple_count != 0 else math.inf
                        path_len += dp_list[-1][ind_in_prev][0]

                        # Update the new layer of DP
                        if path_len <= new_layer_in_dp[ind_in_now][0]:
                            new_layer_in_dp[ind_in_now][0] = path_len
                            new_layer_in_dp[ind_in_now][1] = dp_list[-1][ind_in_prev][1] + now_hanzi
            
            # Push the new layer to DP list
            dp_list.append(new_layer_in_dp)
        
        output_handler.write(dp_list[-1][0][1].replace('^', '').replace('$', '') + '\n')

if __name__ == '__main__':
    main()
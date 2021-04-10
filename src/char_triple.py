import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import math

input_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/sandbox/input.txt'
output_file_path = '/Users/ashitemaru/Downloads/CodingFolder/SophomoreSpring/pinyin/data/sandbox/output.txt'

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

    # Load the dict of weights
    weight_dict = get_weight_dict()

    # Get the hanzi str from pinyin
    for pinyin_str in input_handler.readlines():

        # Start the pinyin str with a ^^, end the pinyin str with a $$
        pinyin_list = ['^', '^']
        pinyin_list += pinyin_str.split(' ')
        pinyin_list[-1] = pinyin_list[-1].replace('\n', '')
        pinyin_list += ['$', '$']
        
        # Start the DP with empty list
        dp_list = [[] for _ in range(len(pinyin_list))]
        dp_list[0] = [0]

        # Set up the path list
        path_list = [[] for _ in range(len(pinyin_list))]
        path_list[0] = [-1]

        # Translate every pinyin from the pinyin str
        for ind_in_str, pinyin in enumerate(pinyin_list):

            # Skip the starting char
            if ind_in_str == 0:
                continue

            # Get the available hanzi
            now_hanzi_list = mapping[pinyin] if pinyin != '$' else ['$']
            prev_hanzi_list = mapping[pinyin_list[ind_in_str - 1]]

            # Init the dp_list of this layer
            dp_list[ind_in_str] = [math.inf for _ in range(len(now_hanzi_list))]
            path_list[ind_in_str] = [-1 for _ in range(len(now_hanzi_list))]

            # The double loop is for traversing the pairs of (prev_char, now_char)
            # This is the process of DP
            for ind_in_now_candidates, now_char in enumerate(now_hanzi_list):
                for ind_in_prev_candidates, prev_char in enumerate(prev_hanzi_list):

                    # Get the weights dict of doubles started by the prev_char
                    weights = weight_dict.get(prev_char, None)
                    if weights == None:
                        continue

                    # Get the counts and the len of the path
                    double_count = weights.get(prev_char + now_char, 0)
                    tot_count = weights['total']
                    path_len = -math.log(double_count / tot_count) if double_count != 0 else math.inf
                    path_len += dp_list[ind_in_str - 1][ind_in_prev_candidates]

                    # Update the dp_list
                    if path_len <= dp_list[ind_in_str][ind_in_now_candidates]:
                        dp_list[ind_in_str][ind_in_now_candidates] = path_len
                        path_list[ind_in_str][ind_in_now_candidates] = ind_in_prev_candidates

        # Use the data of DP to get the path list
        final_path_list = []
        now_loc = 0
        for i in range(len(pinyin_list)):
            final_path_list.append(path_list[-i - 1][now_loc])
            now_loc = path_list[-i - 1][now_loc]
        final_path_list = final_path_list[: : -1][2: ]

        # Transfer
        hanzi_str = ''
        for i, ind in enumerate(final_path_list):
            hanzi_str += mapping[pinyin_list[i + 1]][ind]
        output_handler.write(hanzi_str + '\n')

if __name__ == '__main__':
    main()
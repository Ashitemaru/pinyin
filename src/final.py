import sys

sys.path.append('/usr/local/lib/python3.8/site-packages/')

from tqdm import tqdm
import json
import math

input_file_path = ''
output_file_path = ''
mapping_file_path = ''
double_json_path = ''
triple_json_path = ''

smooth_param = 1 - 1e-4
dt_param = 0.8

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

def get_double_weight_dict():
    json_handle = open(double_json_path, 'r')
    json_pack = json.loads(json_handle.readlines()[0].replace('\'', '\"'))
    tot = 0
    for key in tqdm(json_pack.keys()):
        tot += json_pack[key]['total']
    return json_pack, tot

def get_triple_weight_dict():
    json_handle = open(triple_json_path, 'r')
    json_pack = json.loads(json_handle.readlines()[0].replace('\'', '\"'))
    tot = 0
    for key in tqdm(json_pack.keys()):
        tot += json_pack[key]['total']
    return json_pack, tot

def main():
    if len(sys.argv) != 6:
        print('Error!')
        return

    global input_file_path, output_file_path, mapping_file_path, double_json_path, triple_json_path
    input_file_path, output_file_path, mapping_file_path, double_json_path, triple_json_path = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]

    input_handler = open(input_file_path, 'r')
    output_handler = open(output_file_path, 'w')

    # Load the map from pinyin to hanzi
    mapping = get_mapping()
    mapping['^'] = ['^']
    mapping['$'] = ['$']
    print('Mapping ready!')

    # Load the dict of weights
    double_weight_dict, double_tot = get_double_weight_dict()
    print('Double dictionary ready!')
    triple_weight_dict, triple_tot = get_triple_weight_dict()
    print('Triple dictionary ready!')

    # Get the hanzi str from pinyin
    for pinyin_str in tqdm(input_handler.readlines()):

        # Start the pinyin str with a ^, end the pinyin str with a $
        pinyin_list = ['^', '^']
        pinyin_list += pinyin_str.split(' ')
        pinyin_list[-1] = pinyin_list[-1].replace('\n', '')
        
        # Start the DP with empty list
        # The tuple: (prefix, path_len)
        dp_state = [[['^^', 0]]]

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
            new_dp_state = [
                [['', math.inf] for i in range(len(now_legal_hanzi))]
                    for j in range(len(prev_legal_hanzi))
            ]

            for ind_in_now, now_hanzi in enumerate(now_legal_hanzi):
                for ind_in_pprev, pprev_hanzi in enumerate(pprev_legal_hanzi):
                    for ind_in_prev, prev_hanzi in enumerate(prev_legal_hanzi):

                        # Get the weights dict of doubles started by the prev_hanzi
                        double_weights = double_weight_dict.get(prev_hanzi, {'total': 0})
                        triple_weights = triple_weight_dict.get(pprev_hanzi + prev_hanzi, {'total': 0})

                        def get_path_len(tuple_count, prefix_count, corpus_count, corpus):
                            suffix_count = corpus.get(now_hanzi, {'total': 0})['total']
                            if tuple_count:
                                return tuple_count / prefix_count * smooth_param + suffix_count / corpus_count * (1 - smooth_param)
                            elif suffix_count:
                                return suffix_count / corpus_count * (1 - smooth_param)
                            else:
                                return 0

                        # Get the counts and the len of the path
                        triple_tuple_count = triple_weights.get(pprev_hanzi + prev_hanzi + now_hanzi, 0)
                        triple_tot_count = triple_weights['total']
                        triple_path_len = get_path_len(triple_tuple_count, triple_tot_count, double_tot, double_weight_dict)

                        double_tuple_count = double_weights.get(prev_hanzi + now_hanzi, 0)
                        double_tot_count = double_weights['total']
                        double_path_len = get_path_len(double_tuple_count, double_tot_count, double_tot, double_weight_dict)

                        path_len = -math.log(
                            dt_param * triple_path_len + (1 - dt_param) * double_path_len
                        ) if triple_path_len != 0 and double_path_len != 0 else math.inf
                        path_len += dp_state[ind_in_pprev][ind_in_prev][1]

                        # Update the new layer of DP
                        if path_len < new_dp_state[ind_in_prev][ind_in_now][1]:
                            new_dp_state[ind_in_prev][ind_in_now][1] = path_len
                            new_dp_state[ind_in_prev][ind_in_now][0] = dp_state[ind_in_pprev][ind_in_prev][0] + now_hanzi if len(dp_state[ind_in_pprev][ind_in_prev][0]) else ''
            
            # Push the new layer to DP list
            dp_state = new_dp_state
        
        final = ['', math.inf]
        for sub_list in dp_state:
            for elem in sub_list:
                if elem[1] < final[1]:
                    final = elem
        output_handler.write((final[0].replace('^', '') if final[0] else '烫' * (len(pinyin_list) - 2)) + '\n')

if __name__ == '__main__':
    main()
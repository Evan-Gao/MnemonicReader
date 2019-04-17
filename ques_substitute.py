# Finally, substitute generated questions into squad
# and test BiDAF/RNET performance on easy/hard questions

import ujson as json
import pickle
import argparse
import os
from tqdm import tqdm
import numpy as np
import copy
from collections import defaultdict

parser = argparse.ArgumentParser(
    description='Finally, substitute generated questions into squad and'
                ' test BiDAF/RNET performance on easy/hard questions'
)
parser.add_argument('--generated_file', type=str,
                    default='/research/king2/yfgao/pycharm_deployment/dicoqg/data/generated/wchen_translate_ans_20_one_rposi_0_gold_diff_0_attn_reusecopy.out',
                    help='where to load generated questions')
parser.add_argument('--squad_file', type=str,
                    default='/research/king2/yfgao/pycharm_deployment/dicoqg/data/dicoqg_test.json',
                    help='where to load squad related data')
parser.add_argument('--ques_list_file', type=str, default='/research/king2/yfgao/pycharm_deployment/dicoqg/data/question-id-test.txt',
                    help='where to load generated question ids')
parser.add_argument('--out_suffix', type=str, default='ans20_1rposi0',
                    help='output squad easy/hard file name')
args = parser.parse_args()

# load data...
with open(args.generated_file, 'r', encoding='utf-8') as fh:
    ques_pred = fh.read().splitlines()
with open(args.squad_file, 'r') as fh:
    squad_data = json.load(fh)
with open(args.ques_list_file, 'r') as fh:
    ques_gen_id = fh.read().splitlines()

id2predQ = {}
for id, pred in zip(ques_gen_id, ques_pred):
    id2predQ[id] = pred

# 1. test generated num of lines = gold num of lines
assert len(ques_gen_id) == len(ques_pred), 'num of generated questions mismatch!'

# # 2. validate relationship between ids and gold and squad_data
# matched_squad_ques = 0
# for article in squad_data:
#     for para in article['paragraphs']:
#         for qas in para['qas']:
#             if qas['id'] in question_dict:
#                 matched_squad_ques += 1
# assert matched_squad_ques == len(ques_gen_id), 'num of target questions mismatch!'


# 3. substitute original squad, keep Q&A which generates questions only, turn it into easy and hard file, and save
squad_easy = []
easy_count = 0
for article in tqdm(squad_data):
    squad_easy_article = {}
    squad_easy_article['title']=article['title']
    squad_easy_article['paragraphs'] = []
    for para in article['paragraphs']:
        squad_easy_para = {}
        squad_easy_para['context'] = para['context']
        squad_easy_para['qas'] = []
        for qas in para['qas']:
            if qas['id'] in ques_gen_id:
                if qas['difficulty'] == 0:
                    easy_count += 1
                    qas['question'] = id2predQ[qas['id']]
                    squad_easy_para['qas'].append(qas)
        if len(squad_easy_para['qas']) > 0:
            squad_easy_article['paragraphs'].append(squad_easy_para)
    if len(squad_easy_article['paragraphs']) > 0:
        squad_easy.append(squad_easy_article)
print('copy {} original easy questions from squad_data'.format(easy_count))

squad_easy_count = 0
for article in squad_easy:
    for para in article['paragraphs']:
        squad_easy_count += len(para['qas'])
print('validate: original easy questions {}'.format(squad_easy_count))

squad_hard = []
hard_count = 0
for article in tqdm(squad_data):
    squad_hard_article = {}
    squad_hard_article['title']=article['title']
    squad_hard_article['paragraphs'] = []
    for para in article['paragraphs']:
        squad_hard_para = {}
        squad_hard_para['context'] = para['context']
        squad_hard_para['qas'] = []
        for qas in para['qas']:
            if qas['id'] in ques_gen_id:
                if qas['difficulty'] == 1:
                    hard_count += 1
                    qas['question'] = id2predQ[qas['id']]
                    squad_hard_para['qas'].append(qas)
        if len(squad_hard_para['qas']) > 0:
            squad_hard_article['paragraphs'].append(squad_hard_para)
    if len(squad_hard_article['paragraphs']) > 0:
        squad_hard.append(squad_hard_article)
print('copy {} original hard questions from squad_data'.format(hard_count))

squad_hard_count = 0
for article in squad_hard:
    for para in article['paragraphs']:
        squad_hard_count += len(para['qas'])
print('validate: original hard questions {}'.format(squad_hard_count))

with open(args.out_suffix + '_easy.json', 'w', encoding='utf-8') as fh:
    json.dump(squad_easy, fh)
with open(args.out_suffix + '_hard.json', 'w', encoding='utf-8') as fh:
    json.dump(squad_hard, fh)
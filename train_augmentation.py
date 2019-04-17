# augment training file with qg generated data
import os
import ujson as json

def load_json(loadpath, loadinfo):
    with open(loadpath, 'r', encoding='utf-8') as fh:
        print(loadinfo)
        dataset = json.load(fh)
        print('load json done')
    return dataset


def dump_json(data, savepath, saveinfo):
    with open(savepath, 'w', encoding='utf-8') as fh:
        print(saveinfo)
        json.dump(data, fh)
        print('json save done')


datadir = '/research/king3/yfgao/pd/MnemonicReader/data'
traindir = os.path.join(datadir, 'datasets', 'dicoqg_train.json')
qgeasydir = os.path.join(datadir, 'squadout/ans_0_two_rposi_50_init_diff_10', 'squad_easy.json')
qgharddir = os.path.join(datadir, 'squadout/ans_0_two_rposi_50_init_diff_10', 'squad_hard.json')
qgreverseeasydir = os.path.join(datadir, 'squadout/ans_0_two_rposi_50_init_diff_10', 'squad_reverse_easy.json')
qgreverseharddir = os.path.join(datadir, 'squadout/ans_0_two_rposi_50_init_diff_10', 'squad_reverse_hard.json')

train = load_json(traindir, 'load train')
qgeasy = load_json(qgeasydir, 'load qgeasy')
qghard = load_json(qgharddir, 'load qghard')
qgreverseeasy = load_json(qgreverseeasydir, 'load reverse easy')
qgreversehard = load_json(qgreverseharddir, 'load reverse hard')

train_aug = train + qgeasy + qghard + qgreverseeasy + qgreversehard

trainaugdir = os.path.join(datadir, 'datasets', 'dicoqg_trainaug.json')
dump_json(train_aug, trainaugdir, 'saving train aug')

print('debug')
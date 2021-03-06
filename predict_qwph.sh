#!/usr/bin/env bash
export CUDA_VISIBLE_DEVICES=$1

SUFFIX='ans_0_one_rposi_50_gold_diff_0'
echo ${SUFFIX}

mkdir -p /research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}

python -u ques_substitute.py \
--generated_file=/research/king3/yfgao/pd/MnemonicReader/data/qgout/wchen_translate_${SUFFIX}_attn_reusecopy.out \
--squad_file=/research/king3/yfgao/pd/MnemonicReader/data/datasets/dicoqg_test.json \
--ques_list_file=/research/king3/yfgao/pd/MnemonicReader/data/qgout/question-id-test.txt \
--out_suffix=/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad

echo "Easy"
python -u predict.py \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_easy.json \
--model=/research/king3/yfgao/pd/MnemonicReader/data/models/m_reader.mdl \
--out-dir=/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX} \
--num-workers=10 \
--gpu=0

python -u evaluate-v1.1.py \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_easy.json \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_easy-m_reader.preds

echo "Hard"
python -u predict.py \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_hard.json \
--model=/research/king3/yfgao/pd/MnemonicReader/data/models/m_reader.mdl \
--out-dir=/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX} \
--num-workers=10 \
--gpu=0

python -u evaluate-v1.1.py \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_hard.json \
/research/king3/yfgao/pd/MnemonicReader/data/squadout/${SUFFIX}/squad_hard-m_reader.preds


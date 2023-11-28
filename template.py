import pandas as pd
import json

template = {'x': [], 'y': [], 'customdata': [], 'mode': 'markers', 'opacity': 0.9,
            'hovertemplate': "cat=C. elegans\u003cbr\u003ex=%{x}\u003cbr\u003ey=%{y}\u003cbr\u003egene=%{"
                             "customdata}\u003cextra\u003e\u003c\u002fextra\u003e",
            "legendgroup": "", "name": "", "type": "scattergl"}
data = pd.read_csv(r"D:\ADAMS-model\seq_homo.csv")
data_cele = data[data['cat'] == 'C. elegans']
data_cele_no = data[data['cat'] == 'C. elegans no homologue']
data_hu = data[data['cat'] == 'Human']
data_ch = data[data['cat'] == 'Chlamy']
t_c, t_c_n, t_h, t_ch = template.copy(), template.copy(), template.copy(), template.copy()
t_c['x'] = data_cele['x'].to_list()
t_c['y'] = data_cele['y'].to_list()
t_c['customdata'] = [n for n in data_cele['gene'].to_list()]
t_c['name'] = 'C. elegans'
t_c['marker'] = {}
t_c['marker']['color'] = data_cele['label'].to_list()  # here
t_c['marker']['symbol'] = 'circle-x'
t_c['marker']['colorscale'] = [[0, '#4e2472'], [1 / 600, '#ffeed1'], [2 / 6, '#de406e'], [3 / 6, '#ff9f6e'],
                               [4 / 6, '#a6e8a1'], [5 / 6, '#51c7bb'], [1, '#138bb9'], ]
t_c['marker']['size'] = 10
t_c['legendgroup'] = 'C.elegans'
t_c['hovertemplate'] = "cat=C. elegans\u003cbr\u003ex=%{x}\u003cbr\u003ey=%{y}\u003cbr\u003egene=%{" \
                       "customdata}\u003cextra\u003e\u003c\u002fextra\u003e"

t_c_n['x'] = data_cele_no['x'].to_list()
t_c_n['y'] = data_cele_no['y'].to_list()
t_c_n['customdata'] = [n for n in data_cele_no['gene'].to_list()]
t_c_n['name'] = 'C. elegans no homologue'
t_c_n['marker'] = {}
t_c_n['marker']['color'] = data_cele_no['label'].to_list()  # here
t_c_n['marker']['symbol'] = 'x'
t_c_n['marker']['colorscale'] = [[0, '#4e2472'], [1 / 600, '#ffeed1'], [2 / 6, '#de406e'], [3 / 6, '#ff9f6e'],
                                 [4 / 6, '#a6e8a1'], [5 / 6, '#51c7bb'], [1, '#138bb9'], ]
t_c_n['marker']['size'] = 10
t_c_n['legendgroup'] = 'C. elegans no homologue'
t_c_n['hovertemplate'] = "cat=C. elegans no homologue\u003cbr\u003ex=%{x}\u003cbr\u003ey=%{y}\u003cbr\u003egene=%{" \
                         "customdata}\u003cextra\u003e\u003c\u002fextra\u003e"

t_h['x'] = data_hu['x'].to_list()
t_h['y'] = data_hu['y'].to_list()
t_h['customdata'] = [n for n in data_hu['gene'].to_list()]
t_h['name'] = 'Human'
t_h['marker'] = {}
t_h['marker']['color'] = data_hu['label'].to_list()  # here
t_h['marker']['symbol'] = 'diamond'
t_h['marker']['colorscale'] = [[0, '#4e2472'], [1 / 600, '#ffeed1'], [2 / 6, '#de406e'], [3 / 6, '#ff9f6e'],
                               [4 / 6, '#a6e8a1'], [5 / 6, '#51c7bb'], [1, '#138bb9'], ]
t_h['marker']['size'] = 10
t_h['legendgroup'] = 'Human'
t_h['hovertemplate'] = "cat=Human\u003cbr\u003ex=%{x}\u003cbr\u003ey=%{y}\u003cbr\u003egene=%{" \
                       "customdata}\u003cextra\u003e\u003c\u002fextra\u003e"

t_ch['x'] = data_ch['x'].to_list()
t_ch['y'] = data_ch['y'].to_list()
t_ch['customdata'] = [n for n in data_hu['gene'].to_list()]
t_ch['name'] = 'Chlamydomonas'
t_ch['marker'] = {}
t_ch['marker']['color'] = data_ch['label'].to_list()  # here
t_ch['marker']['symbol'] = 'cross'
t_ch['marker']['colorscale'] = [[0, '#4e2472'], [1 / 600, '#ffeed1'], [2 / 6, '#de406e'], [3 / 6, '#ff9f6e'],
                                [4 / 6, '#a6e8a1'], [5 / 6, '#51c7bb'], [1, '#138bb9'], ]
t_ch['marker']['size'] = 10
t_ch['legendgroup'] = 'Chlamydomonas'
t_ch['hovertemplate'] = "cat=Chlamydomonas\u003cbr\u003ex=%{x}\u003cbr\u003ey=%{y}\u003cbr\u003egene=%{" \
                        "customdata}\u003cextra\u003e\u003c\u002fextra\u003e"

data = [t_c_n, t_c, t_h, t_ch]

with open('./') as f:  # address
    json.dump(data, f)

import pickle as pkl
from tqdm import tqdm

with open('./3.pkl', 'rb') as f:
    data = pkl.load(f)

for i in tqdm(data.items()):
    with open("/home/data3/ALPHAFOLD2/result/tools/ADAMS/mix_db/mx_db/{}_ch.pkl", "wb") as f:
        pkl.dump(i, f)

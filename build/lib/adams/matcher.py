"""
Direct-extract-from-SAM-file
    Copyright (C) 2023
    2q3

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import pandas as pd

from adams.tool_kit import *
import cupy as cp
from scipy.spatial import distance_matrix as dm
import numpy as np
from tqdm import tqdm
import os
import pickle as pkl


class ADAMS_match():
    def __init__(self, ref, threshold=0.95):
        self.ref = ref
        self.features = cp.array([])
        self.distance_matrix = np.array([])
        self.threshold = threshold
        self.extract_features()

    def extract_features(self):
        ca = get_coordinate(self.ref, 'X')
        dist = dm(ca, ca)
        features = extract_features(dist)
        features = norm(features)
        self.distance_matrix = dist
        self.features = cp.array(features)

    def match(self, db_folder):
        content = []
        mempool = cp.get_default_memory_pool()
        mempool.set_limit(size=6 * 1024 ** 3)
        files = os.listdir(db_folder)
        config_path = os.path.join(db_folder, [n for n in files if n[-6:] == 'config'][0])
        with open(config_path, 'r') as f:
            database_list = f.readlines()
        print('{} PARTS OF THE DATABASE WAITING FOR COMPARISON'.format(len(database_list)))
        result = []
        database_list = [n[:-1] for n in database_list]
        for i in database_list:
            with open(os.path.join(db_folder, i), 'rb') as f:
                database = pkl.load(f)
            with open(os.path.join(db_folder, i[:-4] + '_len.pkl'), 'rb') as f:
                length = pkl.load(f)
            data = list(database.items())
            for i in tqdm(data):
                result.append(compare(self.features, self.threshold, i, length))
            mempool.free_all_blocks()
            del database, data
        result = np.asarray(result)
        result = pd.DataFrame(result, columns='protein,match,score,feat_q,feat_k,aa_length'.split(','))
        match = np.asarray(result['match'].values)
        score = np.asarray(result['score'].values)
        match_z = z_score(match)
        score_z = z_score(score)
        result['match_z-score'] = match_z
        result['score_z-score'] = score_z
        result['z-score'] = match_z + score_z
        result.sort_values(by='z-score', ascending=False)
        return result

        # with open(out, 'w+') as f:
        #     f.write('protein,match,score,feat_q,feat_k,aa_length\n')
        #     for i in result:
        #         if i[0] != '0':
        #             try:
        #                 f.write(i)
        #             except:
        #                 continue

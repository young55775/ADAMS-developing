"""
Direct-extract-from-SAM-file
    Copyright (C) 2023  Guo Zhengyang

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
from adams.tool_kit import *
import os
from scipy.spatial import distance_matrix
import cupy as cp
import pickle as pkl
from tqdm.contrib.concurrent import process_map
from functools import partial

def get_feature_list(pdb_folder, file):
    error = []
    try:
        ca = get_coordinate(os.path.join(pdb_folder, file), 'X')
        name = file[:-4]
        dist = distance_matrix(ca, ca)
        dist = extract_features(dist)
        dist = norm(dist)
        length = len(ca)
        return (name, dist, length)
    except:
        error.append('1')
        return ('error', 0, 0)


class DatabaseMaker():
    def __init__(self, device=0, chunk_size=5000, process=40):
        self.device = device
        self.chunk_size = chunk_size
        self.process = process

    def make(self, pdb_folder, out_perfix):
        mempool = cp.get_default_memory_pool()
        files = os.listdir(pdb_folder)
        chunks = len(files) // self.chunk_size
        print('total_chunks = {}'.format(chunks + 1))
        feature_p = partial(get_feature_list, pdb_folder)
        db_list = []
        for i in range(chunks + 1):
            feature_dict = {}
            length_dict = {}
            file = files[self.chunk_size * i:self.chunk_size * i + self.chunk_size]
            result = process_map(feature_p, file, max_workers=self.process, chunksize=1)
            for j in range(len(result)):
                feature_dict[result[j][0]] = cp.asarray(result[j][1])
                length_dict[result[j][0]] = cp.asarray(result[j][2])
            db_list.append('./{}.pkl'.format(i))
            with open(out_perfix + '{}.pkl'.format(i), 'wb') as f:
                pkl.dump(feature_dict, f)
            with open(out_perfix + '{}_len.pkl'.format(i), 'wb') as f:
                pkl.dump(length_dict, f)
            mempool.free_all_blocks()
        with open(out_perfix + '.config', 'w+') as f:
            for i in db_list:
                f.write(i + '\n')
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
from tool_kit import *
import os
from scipy.spatial import distance_matrix
import cupy as cp

def db_maker(pdb_folder, out, mode='compatible'):
    files = os.listdir(pdb_folder)
    data_dict = {}
    if mode == 'compatible':
        data_dict['mode'] = 'compatible'
    if mode == 'cuda':
        data_dict['mode'] = 'cuda'
    for i in files:
        name_lst = []
        length_lst = []
        feature_lst = []
        if i[:-3] == 'pdb':
            try:
                ca = get_coordinate(os.path.join(pdb_folder, i), 'X')
                dist = distance_matrix(ca, ca)
                dist = extract_features(dist)
                dist = norm(dist)
                if mode == 'compatible':
                    data_dict[i[:-4]] = dist
                if mode == 'cuda':
                    data_dict[i[:-4]] = cp.asarray(dist)
                name_lst.append(i[:-4])
                length_lst.append(len(ca))
                feature_lst.append(dist.shape[0])
            except:
                raise  ValueError(f'{i} can not be parsed')
    with open(out, 'wb') as f:
        pkl.dump(data_dict, f)
    with open(out + '_report.csv','w') as f:
        f.write('name,aa_length,feature_length\n')
        for i in range(len(name_lst)):
            f.write(f"{name_lst[i]},{length_lst[i]},{feature_lst[i]}\n")


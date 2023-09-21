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

from tool_kit import *
import cupy as cp
from cupyx.scipy.spatial import distance_matrix
from scipy.spatial import distance_matrix as dm
import numpy as np
from functools import partial
from tqdm.contrib.concurrent import process_map
from tqdm import tqdm

def compare(des, t, data):
    # try:
    #dt = cp.asarray(data[1])
    dist = cp.dot(des, data[1].T)
    n = cp.sum(cp.sum(dist > float(t), axis=1) > 0)
    return f"{data[0]},{n}\n"

def compare_c(des, t, data):
    # try:
    #dt = cp.asarray(data[1])
    dist = np.dot(des, data[1].T)
    n = np.sum(np.sum(dist > float(t), axis=1) > 0)
    return f"{data[0]},{n}\n"

def matcher(db, ref, out, t=0.95, core=1, chunk=100):
    d = open(db, 'rb')
    data = pkl.load(d)
    d.close()
    data = list(data.items())
    ca = get_coordinate(ref, 'X')
    mat = dm(ca, ca)
    content = []
    mat = cv2.normalize(mat, None, 0, 255, cv2.NORM_MINMAX).astype('uint8')
    des = extract_features(mat)
    des = norm(des)
    if data['mode'] == 'cuda':
        des = cp.asarray(des)
        compare_partial = partial(compare, des, t)
        for i in tqdm(data):
            if i[0] != 'mode'
            content.append(compare_partial(i))
        #    content = process_map(compare_partial,data,chunksize = chunk, max_workers = core)
        with open(out, 'w+') as f:
            f.write('protein,match\n')
            for i in content:
                try:
                    f.write(i)
                except:
                    continue
    else:
        raise Warning('CPU is super slow in current code')
        compare_partial = partial(compare_c, des, t)
        data = [n for n in data if n[0] != 'mode']
        for i in tqdm(data):
            content = process_map(compare_partial,data,chunksize = chunk, max_workers = core)
        with open(out, 'w+') as f:
            f.write('protein,match\n')
            for i in content:
                try:
                    f.write(i)
                except:
                    continue


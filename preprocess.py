import argparse
import os
import sys
import re
import pandas as pd
from itertools import takewhile

def preprocess():

    listmpaVersion = set()
    merged_tables = pd.DataFrame()

    for f in os.listdir('profile/'):
        if f[15:17]=="PD":
            f = os.path.joi('profile/', f)
            with open(f) as fin:
                headers = [x.strip() for x in takewhile(lambda x: x.startswith('#'), fin)]
            if len(headers) == 1:
                names = ['clade_name', 'relative_abundance']
                index_col = 0
            if len(headers) >= 4:
                names = headers[-1].split('#')[1].strip().split('\t')
                index_col = [0,1]

            mpaVersion = list(filter(re.compile('#mpa_v[0-9]{2,}_CHOCOPhlAn\w*/{0,3}_[0-9]{0,}').match, headers))
            if len(mpaVersion):
                listmpaVersion.add(mpaVersion[0])
            else:
                print('merge_metaphlan_tables found tables without a header including the database version. Exiting.\n')
                return
            if len(listmpaVersion) > 1:
                print('merge_metaphlan_tables found tables made with different versions of the MetaPhlAn database.\nPlease re-run MetaPhlAn with the same database.\n')
                return
            
            iIn = pd.read_csv(f, 
                            sep='\t',
                            skiprows=len(headers),
                            names = names,
                            usecols=range(3),
                            ).fillna('')
            iIn = iIn.set_index(iIn.columns[index_col].to_list())
            if merged_tables.empty:
                merged_tables = iIn.iloc[:,0].rename(os.path.splitext(os.path.basename(f))[0]).to_frame()
            else:
                merged_tables = pd.merge(iIn.iloc[:,0].rename(os.path.splitext(os.path.basename(f))[0]).to_frame(),
                                        merged_tables,
                                        how='outer', 
                                        left_index=True, 
                                        right_index=True
                                        )
        with open('pd_merged.txt', 'w') as fout:
            if listmpaVersion:
                fout.write(list(listmpaVersion)[0]+'\n')
            merged_tables.fillna('0').reset_index().to_csv(fout, index=False, sep = '\t')

if __name__ == '__main__':
    preprocess()
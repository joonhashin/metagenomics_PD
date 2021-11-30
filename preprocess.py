import os
import numpy as np
import pandas as pd
from tqdm import tqdm

def preprocess(dir = 'PRJEB17784/', out_dir = 'profile_3/'):
    # load labels
    line_count = 0
    id_list = []
    label = {}
    with open('sample_list.txt', 'r') as f:
        for line in f:
            line_data = line.rstrip()
            line_count += 1
            if line_count == 2:
                id = line_data[24:-17]
                id_list.append(id)
            elif line_count == 14:
                sample_label = line_data[19:-4]
                label[id] = sample_label
            elif line_count == 30:
                line_count = 0
    
    df = pd.read_csv('filereport_read_run_PRJEB17784_tsv.txt', sep='\t')
    for id in tqdm(id_list):
        # load fastq file list
        run_list = list(df[df['sample_accession']==id]['run_accession'])

        # run metaphlan
        string = ''
        for run_id in run_list:
            for file_name in os.listdir(os.path.join(dir,run_id)):
                if os.path.splitext(file_name)[1] != '.gz':
                    continue
                file_path = os.path.join(dir, run_id,file_name)
                string += file_path
                string += ','
        sample_label = label[id]

        bowtie = 'bowtie2out/'+id+'.bowtie2.bz2'
        #os.system('metaphlan '+string[:-1]+ ' --bowtie2out bowtie2out/ '+ id+'.bowtie2.bz --input_type fastq > '+out_dir+id+'_'+sample_label+'_profile.txt')
        os.system('metaphlan '+string[:-1]+ ' --bowtie2out '+bowtie+' --input_type fastq > '+out_dir+id+'_'+sample_label+'_profile.txt')


if __name__ =="__main__":
    preprocess()
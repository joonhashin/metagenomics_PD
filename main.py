import data.tutorial.load_data as load_data, preprocess, classify




if __name__ =="__main__":

    input = {
        "filereport" : 'filereport_read_run_PRJEB17784_tsv.txt', 
        "sample_list" : 'sample_list.txt', 
        "dir" : 'data/tutorial/', 
        "out_dir" : 'profile/'
    }

    load_data(**input)
    preprocess()
    classify()

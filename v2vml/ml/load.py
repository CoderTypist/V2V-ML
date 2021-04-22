import pickle


# Use svm as it performed best
def load_svm_hashmap(dir_path) -> dict:

    # Ensure file path ends with /
    if dir_path[-1] != '/':
        dir_path += '/'

    # Create hashmap
    svm_hm = {}

    # Load in each .pkl file created for SVM
    with open(dir_path + '03_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[3] = pickle.load(in_file)

    with open(dir_path + '04_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[4] = pickle.load(in_file)

    with open(dir_path + '05_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[5] = pickle.load(in_file)

    with open(dir_path + '06_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[6] = pickle.load(in_file)

    with open(dir_path + '07_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[7] = pickle.load(in_file)

    with open(dir_path + '08_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[8] = pickle.load(in_file)

    with open(dir_path + '09_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[9] = pickle.load(in_file)

    with open(dir_path + '20_SVM_Model.pkl', 'rb') as in_file:
        svm_hm[10] = pickle.load(in_file)

    return svm_hm

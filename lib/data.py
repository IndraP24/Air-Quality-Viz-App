import os
import shutil
import json
import glob
import kaggle


def load_data(dataset: str):
    with open("/home/indrap24/.kaggle/kaggle.json", "r") as f:
        data = json.load(f)

    os.environ['KAGGLE_USERNAME'] = data['username']
    os.environ['KAGGLE_KEY'] = data['key']

    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, unzip=True)

    src_path = os.getcwd()

    if os.path.exists(src_path):
        dest_path = 'data/'
        for f in os.listdir(dest_path):
            os.remove(os.path.join(dest_path, f))

        for folders, subfolders, files in os.walk(src_path):
            for file in files:
                if file.endswith('{}'.format('.csv')):
                    src = src_path + '/' + file
                    dest = src_path + '/' + dest_path + file
                    shutil.move(src, dest)


load_data('rohanrao/air-quality-data-in-india')

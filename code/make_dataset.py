"""
株価チャートの画像をtrain/validation/test setに分ける
Usage:
    # 全銘柄について
    $ python make_dataset.py
"""
import argparse
import os
import glob
import pathlib
import shutil
import random
from sklearn.model_selection import train_test_split
seed = 42
random.seed(seed)  # 乱数シード固定


def make_dataset(orig_image_dir, dataset_dir):
    """株価チャートの画像をtrain/validation/test setに分ける"""
    # クラスごとにpng画像パス取得
    classes = ['0', '1', '2']
    dir_png_paths = [glob.glob(os.path.join(orig_image_dir, c, '*png')) for c in classes]
    len_dirs = [len(png_paths) for png_paths in dir_png_paths]

    # 一応ランダムに並び替え
    dir_png_paths = [random.sample(png_paths, len(png_paths)) for png_paths in dir_png_paths]

    # ランダムサンプリングして各クラス数合わせる
    dir_png_paths_sampling = [random.sample(png_paths, min(len_dirs)) for png_paths in dir_png_paths]

    # train/vakidation/testに分ける
    val_test_size = 0.2
    test_size = 0.5
    for cla, png_paths in zip(classes, dir_png_paths_sampling):
        _train, _val_test = train_test_split(png_paths,
                                             shuffle=True,
                                             random_state=seed,
                                             test_size=val_test_size)
        _val, _test = train_test_split(_val_test,
                                       shuffle=True,
                                       random_state=seed,
                                       test_size=test_size)
        # 画像コピー
        for p in _train:
            _dir = os.path.join(dataset_dir, 'train', cla)
            os.makedirs(_dir, exist_ok=True)
            copy = os.path.join(_dir, pathlib.Path(p).name)
            shutil.copyfile(p, copy)

        for p in _val:
            _dir = os.path.join(dataset_dir, 'validation', cla)
            os.makedirs(_dir, exist_ok=True)
            copy = os.path.join(_dir, pathlib.Path(p).name)
            shutil.copyfile(p, copy)

        for p in _test:
            _dir = os.path.join(dataset_dir, 'test', cla)
            os.makedirs(_dir, exist_ok=True)
            copy = os.path.join(_dir, pathlib.Path(p).name)
            shutil.copyfile(p, copy)


def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", "--output_dir", type=str,
                    default=r'D:\work\chart_model\output_new\dataset\all')
    ap.add_argument("-i", "--input_dir", type=str,
                    default=r'D:\work\chart_model\output_new\orig_image_all')
    return vars(ap.parse_args())


if __name__ == '__main__':
    args = get_args()
    make_dataset(args['input_dir'], args['output_dir'])
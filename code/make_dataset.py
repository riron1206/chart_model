"""
株価チャートの画像をtrain/validation/test setに分ける
"""
import os
import glob
import pathlib
import shutil
import random
random.seed(42)  # 乱数シード固定


def make_dataset(orig_image_dir, dataset_dir):

    paths_1 = glob.glob(os.path.join(orig_image_dir, '1', '*png'))
    paths_0 = glob.glob(os.path.join(orig_image_dir, '0', '*png'))
    # print([pathlib.Path(p).name for p in paths_1[:5]])

    len_paths_1 = len(paths_1)
    # len_paths_0 = len(paths_0)

    # valid, testは各クラス500枚にしておく
    valid_len, test_len = 500, 500
    train_len = len_paths_1 - valid_len - test_len

    # ランダムに並び替え
    paths_1 = random.sample(paths_1, len(paths_1))
    paths_0 = random.sample(paths_0, len(paths_0))
    # print([pathlib.Path(p).name for p in paths_1[:5]])

    # train/vakidation/testに分ける
    train_paths_1 = paths_1[: train_len]
    valid_paths_1 = paths_1[train_len: train_len + valid_len]
    test_paths_1 = paths_1[train_len + valid_len: len_paths_1]

    train_paths_0 = paths_0[: train_len]
    valid_paths_0 = paths_0[train_len: train_len + valid_len]
    test_paths_0 = paths_0[train_len + valid_len: len_paths_1]

    # train setコピー
    for p in train_paths_1:
        _dir = os.path.join(dataset_dir, 'train', '1')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)

    for p in train_paths_0:
        _dir = os.path.join(dataset_dir, 'train', '0')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)

    # validation set コピー
    for p in valid_paths_1:
        _dir = os.path.join(dataset_dir, 'validation', '1')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)

    for p in valid_paths_0:
        _dir = os.path.join(dataset_dir, 'validation', '0')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)

    # test set コピー
    for p in test_paths_1:
        _dir = os.path.join(dataset_dir, 'test', '1')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)

    for p in test_paths_0:
        _dir = os.path.join(dataset_dir, 'test', '0')
        os.makedirs(_dir, exist_ok=True)
        copy = os.path.join(_dir, pathlib.Path(p).name)
        shutil.copyfile(p, copy)


if __name__ == '__main__':
    orig_image_dir = r'C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output\orig_image'
    dataset_dir = r'C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output\dataset\JPX日経インデックス400+日経225+日経500'
    make_dataset(orig_image_dir, dataset_dir)
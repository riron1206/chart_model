# チャート画像から株価予想するモデル
- 参考: https://note.com/inoichan/n/n97d0944d4e7d
- ※株価データベースと株価csvが必要

## 行った手順
1. notebook/make_chart.ipynb でデータ作成試す
1. notebook/make_tf_model.*.ipynb でモデル作成試す
1. code/make_chart.py でチャート画像作成
```bash
$ python make_chart.py
$ python make_chart_all.py
```
1. code/make_dataset.py でデータセット作成
```bash
$ python make_dataset.py
$ python make_dataset.py -o D:\work\chart_model\output\dataset\all -i D:\work\chart_model\output\orig_image_all
```
1. code/tf_base_class*.py でモデル作成+パラメータチューニング
```bash
$ python tf_base_class.py -m train
$ python tf_base_class.py -m tuning -n_t 15 -t_out_dir D:\work\chart_model\output\model\tf_base_class_py\optuna
$ python tf_base_class_optuna_Xception.py -m tuning -n_t 200 -t_out_dir D:\work\chart_model\output\model\tf_base_class_py\optuna_Xception
```

### 出力ファイルディレクトリはDドライブにコピーしてシンボリックリンク付けた
```bash
$ mklink /d "C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output" "D:\work\chart_model\output"
```
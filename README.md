# チャート画像から株価予想するモデル

![sample_chart.png](https://github.com/riron1206/chart_model/blob/master/sample_chart.png)

- 参考: https://note.com/inoichan/n/n97d0944d4e7d
- 株価データベースと株価csvが必要
	- https://github.com/riron1206/03.stock_repo/tree/master/sqlite_analysis
- 02_keras_pyライブラリも必要
	- https://github.com/riron1206/02_keras_py
- 出力ファイルディレクトリはDドライブにコピーしてシンボリックリンク付けた
	- Powershellではmklink使えないのでコマンドプロンプトで実行すること
```bash
$ mklink /d "C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output_new" "D:\work\chart_model\output_new"
```

## モデルの正解率は0.6ぐらいなのであまりあてにはならない

## 行った手順
#### 1. notebook/*.ipynb でデータ作成、モデル作成試す
#### 2. code/make_chart_all.py でチャート画像作成
```bash
$ python make_chart_all.py
```
#### 3. code/make_dataset.py でデータセット作成
```bash
$ python make_dataset.py
```
#### 4. code/tf_base_class*.py でモデル作成（パラメータチューニングも可能）
```bash
$ python tf_base_class_all_data.py -m train
```
#### 5. bestモデルで予測
- 15日後の終値が最終日の5%以上低ければクラス「1」
- 15日後の終値が最終日の5%以上高ければクラス「2」
- それ以外はクラス「0」
```bash
$ python tf_predict_best_model.py
```

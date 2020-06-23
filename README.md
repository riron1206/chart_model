# チャート画像から株価予想するモデル
- 参考: https://note.com/inoichan/n/n97d0944d4e7d

## 手順
1. notebook/make_chart.ipynb でデータ作成試す
1. notebook/make_tf_model.*.ipynb でモデル作成試す
1. code/make_chart.py でチャート画像作成
1. code/make_dataset.py でデータセット作成
1. code/tf_base_class.py でモデル作成

### 出力ファイルディレクトリはDドライブにコピーしてシンボリックリンク付けた
```bash
$ mklink /d "C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output" "D:\work\chart_model\output"
```
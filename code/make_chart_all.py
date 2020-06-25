"""
全銘柄コードについて株価チャートの画像作成
- https://note.com/inoichan/n/n97d0944d4e7d
Usage:
    $ python make_chart_all.py
"""
import os
import glob
import sqlite3
import datetime
# import traceback
import pathlib

import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

import warnings
warnings.filterwarnings("ignore")


def table_to_df(table_name=None, sql=None, db_file_name=r'D:\DB_Browser_for_SQLite\stock.db'):
    """sqlite3で指定テーブルのデータをDataFrameで返す"""
    conn = sqlite3.connect(db_file_name)
    if table_name is not None:
        return pd.read_sql(f'SELECT * FROM {table_name}', conn)
    elif sql is not None:
        return pd.read_sql(sql, conn)
    else:
        return None


def get_code_close(code, start_date, end_date):
    """DBから指定銘柄の株価取得"""
    sql = f"""
    SELECT
        t.date,
        t.close
    FROM
        prices AS t
    WHERE
        t.code = {code}
    AND
        t.date >= '{start_date}'
    AND
        t.date <= '{end_date}'
    """
    return table_to_df(sql=sql)


def make_chart(code, start_date, end_date, output_dir=None):
    """株価チャートの画像作成"""

    # 移動平均線とるのでだいぶ前からデータ取得
    start_date_sql = start_date - datetime.timedelta(days=120)
    df = get_code_close(code, str(start_date_sql), str(end_date))

    # 移動平均線
    df['25MA'] = df['close'].rolling(window=25).mean()
    df['75MA'] = df['close'].rolling(window=75).mean()

    # 余分なレコード削除
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['date'] >= d_start_date]
    df = df.dropna()
    df = df.set_index('date', drop=False)

    # 最終日から15日後の株価取得し、15日後の株価が最終日の5%以上高ければ「1」低ければ「0」のラベルを付ける
    last_date = df.iloc[-1]['date'].date()
    df_last_date = get_code_close(code, str(last_date), str(last_date + datetime.timedelta(days=15)))
    label = 0
    if df_last_date.iloc[0]['close'] * 1.05 < df_last_date.iloc[-1]['close']:
        label = 1

    # 80レコードなければチャート出さない
    if df.shape[0] >= 80:
        xdate = [x.date() for x in df.index]
        plt.figure(dpi=100, figsize=(1.5, 1.5))
        plt.plot(xdate, df['close'], color='red', linestyle='solid', linewidth=0.7)
        plt.plot(xdate, df['25MA'], color='green', linestyle='solid', linewidth=0.7)
        plt.plot(xdate, df['75MA'], color='blue', linestyle='solid', linewidth=0.7)
        plt.tick_params(labelbottom=False,
                        labelleft=False,
                        labelright=False,
                        labeltop=False)

        if output_dir is not None:
            # ラベルごとにディレクトリ分ける
            output_dir = os.path.join(output_dir, str(label))
            output_png = os.path.join(output_dir, str(code) + '_' + str(start_date) + '_' + str(end_date) + '.png')
            plt.savefig(output_png)

        plt.show()

    return df


if __name__ == '__main__':
    output_dir = r'C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output\orig_image_all'
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, '0'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, '1'), exist_ok=True)

    # 全銘柄コード
    codes = [pathlib.Path(p).stem for p in glob.glob(r'D:\DB_Browser_for_SQLite\csvs\kabuoji3\*csv')]

    for code in codes:
        start_date = '2000-01-01'
        d_start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        stop_date = '2020-06-10'
        d_stop_date = datetime.datetime.strptime(stop_date, '%Y-%m-%d').date()

        while True:
            d_end_date = d_start_date + datetime.timedelta(weeks=4 * 4 + 2)  # 4ヶ月半後までデータとる
            print(code, d_start_date, d_end_date)

            # この日以降になったら終わらす
            if d_end_date >= d_stop_date:
                break

            try:
                # ファイルあれば飛ばす
                _name = str(code) + '_' + str(d_start_date) + '_' + str(d_end_date) + '.png'
                output_png_0 = os.path.join(output_dir, '0', _name)
                output_png_1 = os.path.join(output_dir, '1', _name)
                if os.path.exists(output_png_0) == False and os.path.exists(output_png_1) == False:

                    # 株価取得
                    df = make_chart(code, d_start_date, d_end_date, output_dir=output_dir)

                    # 80レコード未満なら終わらす
                    if df.shape[0] < 80:
                        break

            except Exception:
                # traceback.print_exc()
                pass

            d_start_date = d_end_date

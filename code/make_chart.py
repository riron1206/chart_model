"""
株価チャートの画像作成
- https://note.com/inoichan/n/n97d0944d4e7d
"""
import os
import sqlite3
import pandas as pd
import datetime
# import traceback

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

    # 最終日から15日後の株価取得し、最終日よりも5%以上高ければ「1」低ければ「0」のラベルを付ける
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
    output_dir = r'C:\Users\81908\jupyter_notebook\tf_2_work\stock_work\chart_model\output\orig_image'

    # JPX日経インデックス400 + 日経225 + 日経500種
    # https://indexes.nikkei.co.jp/nkave/index/component?idx=nk500av
    codes = [1332, 1333, 1379, 1518, 1605, 1662, 1719, 1720, 1721, 1801, 1802, 1803, 1808, 1812, 1820, 1821, 1824,
             1860, 1861, 1878, 1881, 1893, 1911, 1925, 1928, 1942, 1944, 1951, 1959, 1963, 2002, 2121, 2124, 2127,
             2146, 2175, 2181, 2201, 2206, 2212, 2229, 2264, 2267, 2269, 2270, 2282, 2296, 2327, 2331, 2337, 2371,
             2379, 2412, 2413, 2427, 2432, 2433, 2501, 2502, 2503, 2531, 2579, 2587, 2593, 2607, 2651, 2670, 2702,
             2730, 2768, 2782, 2784, 2801, 2802, 2809, 2810, 2811, 2815, 2871, 2875, 2897, 2914, 3003, 3038, 3048,
             3064, 3086, 3088, 3092, 3099, 3101, 3103, 3105, 3107, 3116, 3141, 3148, 3167, 3197, 3231, 3254, 3288,
             3289, 3291, 3349, 3360, 3382, 3391, 3401, 3402, 3405, 3407, 3436, 3543, 3549, 3626, 3632, 3656, 3659,
             3668, 3738, 3765, 3769, 3861, 3863, 3865, 3932, 3938, 3941, 4004, 4005, 4021, 4041, 4042, 4043, 4061,
             4062, 4063, 4088, 4091, 4114, 4118, 4151, 4182, 4183, 4185, 4188, 4202, 4203, 4204, 4205, 4206, 4208,
             4246, 4272, 4307, 4321, 4324, 4403, 4452, 4502, 4503, 4506, 4507, 4516, 4519, 4521, 4523, 4527, 4528,
             4530, 4536, 4540, 4543, 4544, 4555, 4568, 4578, 4581, 4587, 4612, 4613, 4631, 4661, 4666, 4676, 4680,
             4681, 4684, 4689, 4704, 4716, 4732, 4739, 4751, 4755, 4768, 4819, 4849, 4901, 4902, 4911, 4912, 4921,
             4922, 4927, 4967, 4974, 5019, 5020, 5021, 5101, 5105, 5108, 5110, 5201, 5202, 5214, 5232, 5233, 5301,
             5332, 5333, 5334, 5393, 5401, 5406, 5411, 5423, 5444, 5463, 5471, 5486, 5541, 5631, 5703, 5706, 5707,
             5711, 5713, 5714, 5741, 5801, 5802, 5803, 5901, 5929, 5938, 5947, 5975, 5991, 6028, 6098, 6103, 6113,
             6135, 6136, 6141, 6146, 6178, 6201, 6268, 6269, 6273, 6301, 6302, 6305, 6324, 6326, 6361, 6367, 6370,
             6383, 6395, 6412, 6417, 6432, 6448, 6460, 6463, 6465, 6471, 6472, 6473, 6479, 6481, 6501, 6503, 6504,
             6506, 6586, 6588, 6592, 6594, 6632, 6641, 6645, 6674, 6701, 6702, 6703, 6723, 6724, 6727, 6728, 6740,
             6750, 6752, 6753, 6754, 6755, 6758, 6762, 6770, 6806, 6807, 6841, 6845, 6849, 6856, 6857, 6861, 6869,
             6877, 6902, 6920, 6923, 6925, 6952, 6954, 6963, 6965, 6967, 6971, 6976, 6981, 6988, 6995, 7003, 7004,
             7011, 7012, 7013, 7014, 7148, 7164, 7167, 7180, 7181, 7182, 7186, 7189, 7201, 7202, 7203, 7205, 7211,
             7224, 7231, 7240, 7251, 7259, 7261, 7267, 7269, 7270, 7272, 7276, 7282, 7309, 7313, 7419, 7453, 7458,
             7459, 7518, 7532, 7550, 7564, 7575, 7606, 7649, 7701, 7717, 7729, 7731, 7732, 7733, 7735, 7741, 7747,
             7751, 7752, 7762, 7832, 7846, 7867, 7911, 7912, 7915, 7936, 7951, 7956, 7974, 7988, 8001, 8002, 8015,
             8016, 8020, 8028, 8031, 8035, 8053, 8056, 8058, 8060, 8086, 8088, 8111, 8113, 8136, 8227, 8233, 8242,
             8252, 8253, 8267, 8273, 8279, 8282, 8283, 8303, 8304, 8306, 8308, 8309, 8316, 8331, 8334, 8354, 8355,
             8358, 8359, 8369, 8377, 8379, 8382, 8385, 8410, 8411, 8418, 8424, 8439, 8473, 8515, 8524, 8570, 8572,
             8585, 8586, 8591, 8593, 8595, 8601, 8604, 8609, 8616, 8628, 8630, 8697, 8698, 8725, 8729, 8750, 8766,
             8795, 8801, 8802, 8804, 8830, 8848, 8850, 8876, 8905, 9001, 9003, 9005, 9006, 9007, 9008, 9009, 9020,
             9021, 9022, 9024, 9041, 9042, 9044, 9045, 9048, 9062, 9064, 9065, 9076, 9086, 9101, 9104, 9107, 9142,
             9143, 9201, 9202, 9232, 9301, 9303, 9364, 9401, 9404, 9412, 9432, 9433, 9435, 9437, 9449, 9468, 9501,
             9502, 9503, 9504, 9505, 9506, 9507, 9508, 9509, 9513, 9531, 9532, 9533, 9602, 9603, 9613, 9627, 9678,
             9681, 9684, 9697, 9706, 9719, 9735, 9744, 9766, 9783, 9810, 9831, 9843, 9962, 9983, 9984, 9987, 9989]

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

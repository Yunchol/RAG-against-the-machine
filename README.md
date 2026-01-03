step4は評価だから飛ばす
step5もとばす➡︎現場なら、該当するchunkをLLMに渡して文章を生成するだけ



OK。
じゃあ **「venv前提」で、さっきのロードマップをそのまま使える形に書き直す**ね。
**後日これを見れば、今どこにいるか一瞬で分かる版**。

---

# RAG課題・実装ロードマップ（venv版／保存用）

> 目的
>
> * 今どの段階か
> * 次に何をやるか
>   を **迷わず確認できる地図**

---

## まず前提（環境）

### Python仮想環境

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 依存関係

```bash
pip install -r requirements.txt
```

※ `requirements.txt` に

* pydantic
* fire
* tqdm
* bm25s（または sklearn）
* transformers（LLM使う段階で）
  を書く想定。

---

## 全体の流れ（これだけ覚える）

```
Step0: 骨組みだけ作る
Step1: chunkを作る
Step2: 検索（BM25）を通す
Step3: CLIで動かす
Step4: 評価（recall@k）
Step5: LLMで回答
Step6: README & 調整
```

---

## Step0：プロジェクトの骨組み

### やること

* ディレクトリ構成を作る
* CLIが起動するだけにする

### 例

```
src/
 ├─ __main__.py
 ├─ index.py
 ├─ search.py
 ├─ evaluate.py
 └─ models.py
```

### ゴール

```bash
python -m src
```

が **エラーなく起動**

👉 中身は空でOK

---

## Step1：chunkを作る（最重要）

### やること

* vLLMリポジトリを読む
* ファイル種類で分ける

  * `.py`
  * `.md`
* 構造を使って分割

### chunkの最低構成

```python
class Chunk:
    text: str
    file_path: str
    start: int
    end: int
```

### 分け方の指針

* Python：関数 / クラス単位
* Markdown：見出し単位
* 2000文字超えたら分割

### ゴール

* `List[Chunk]` が作れる
* LLMは使っていない

👉 **ここが一番大事**

---

## Step2：検索（BM25 / TF-IDF）

### やること

* 全chunk.textを検索対象にする
* 質問文を入れると
* chunkに点数が付く
* 上位k件が取れる

### ゴール

```python
results = search("OpenAI compatible server", k=5)
```

で `Chunk` が返る

### ポイント

* ベクトル不要
* キーワード抽出不要
* 文章 vs 文章

👉 **検索精度＝合否**

---

## Step3：CLIを完成させる

### やること

Python FireでCLIを作る。

#### index

```bash
python -m src index
```

* chunk作成
* 検索用データ保存

#### search

```bash
python -m src search "質問" --k 10
```

* 検索
* JSON出力（pydantic準拠）

### ゴール

* コマンドが全部通る
* 落ちない

👉 **評価環境が最初に触る場所**

---

## Step4：search_dataset & evaluate

### やること

* 質問JSONをループ処理
* search結果をまとめる
* 正解データと比較
* recall@k計算

### recall判定

* file_path一致
* 文字範囲が **5%以上重なればOK**

### ゴール

```bash
python -m src evaluate result.json answer.json
```

で数値が出る

👉 **ここが一番採点される**

---

## Step5：answer（LLM）

### やること

* 検索で取れたchunkだけを
* LLMに渡す
* 説明文を生成

### ポイント

* LLMは「説明係」
* 根拠はchunkのみ
* 毎回ロードしない

### ゴール

```bash
python -m src answer "質問"
```

で自然文が返る

👉 **評価的には後回しでOK**

---

## Step6：README & 最終調整

### 書くこと

* システム構成
* chunk戦略
* 検索方法
* recall@k
* 工夫した点

### ゴール

* 初見の人が理解できる

---

## 迷ったらこの表を見る

| 今の悩み     | 見るStep    |
| -------- | --------- |
| 何から作る？   | Step0     |
| 検索が当たらない | Step1 / 2 |
| CLI壊れる   | Step3     |
| recall低い | Step4     |
| LLM重い    | Step5     |

---

## 最重要メモ（赤字で）

* **chunk → search → evaluate**
* LLMは最後
* 「動く → 正しい → きれい」

---

## 最後に

この課題は
**順番を守れば必ず完成する**。

このロードマップを
**READMEかメモにそのまま貼って進める**のがおすすめ。

---

次にやるなら自然なのは👇
👉 **Step1：chunk最小実装（Python / Markdown）を書く**
👉 **Step2：BM25を最短コードで動かす**

どっちから行く？

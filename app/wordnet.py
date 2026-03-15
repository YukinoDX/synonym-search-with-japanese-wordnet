import sqlite3


class Word:
    def __init__(self, wordid: int, lang: str, lemma: str, pron, pos: str):
        """
        wordit: 単語ID
        lang: 単語の言語 (sense.langと同じになる？)
        lemma: 単語
        pron: 謎
        pos: 品詞
        """
        self.wordid = wordid
        self.lang = lang
        self.lemma = lemma
        self.pron = pron
        self.pos = pos


class Synset:
    def __init__(self, synset: str, pos: str, name: str, src: str):
        """
        synset: 概念ID
        pos: 品詞
        name: 謎 (概念を表す？英単語)
        src: 謎
        """
        self.synset = synset
        self.pos = pos
        self.name = name
        self.src = src


class Sense:
    def __init__(self, synset: str, wordid: int, lang: str, rank, lexid, freq, src):
        """
        synste: 概念ID
        wordid: 単語ID
        lang: 単語の言語
        rank: 謎
        lexid: 謎
        freq: 謎
        src: 謎
        """
        self.synset = synset
        self.wordid = wordid
        self.lang = lang
        self.rank = rank
        self.lexid = lexid
        self.freq = freq
        self.src = src


class Synsetdef:
    def __init__(self, synset: str, lang: str, def_: str, sid):
        """
        synset:概念ID
        lang:defの言語
        def_:概念の説明
        sid:謎
        """
        self.synset = synset
        self.lang = lang
        self.def_ = def_
        self.sid = sid


class Synlink:
    def __init__(self, synset1: str, synset2: str, link: str, src):
        """
        synset1: 概念ID
        synset2: 概念ID
        link: 関係ID
        src: 謎
        """
        self.synset1 = synset1
        self.synset2 = synset2
        self.link = link
        self.src = src


class WordNet:
    def __init__(self):
        self.conn = sqlite3.connect("db/wnjpn.db", check_same_thread=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def get_synset_by_id(self, id: str):
        return Synset(
            *self.conn.execute(
                "SELECT * FROM synset WHERE synset = ?", (id,)
            ).fetchone()
        )

    def get_synset_by_lemma(self, lemma: str) -> list[Synset]:
        """
        lemma -> Word => Synset
        単語lemmaと紐づくSynsetたちを返す
        """

        word_res = self.conn.execute(
            "SELECT * FROM word WHERE lemma = ?", (lemma,)
        ).fetchone()
        if not word_res:
            return []
        word = Word(*word_res)

        synsets = []
        for row in self.conn.execute(
            "SELECT * FROM sense WHERE wordid = ?", (word.wordid,)
        ).fetchall():
            sense = Sense(*row)
            synset = self.get_synset_by_id(sense.synset)
            synsets.append(synset)

        return synsets

    def get_words_by_synset(self, synset: Synset) -> list[Word]:
        """
        synset => Word
        """
        senses = [
            Sense(*sense)
            for sense in self.conn.execute(
                "SELECT * FROM sense WHERE synset = ?", (synset.synset,)
            ).fetchall()
        ]
        words = [
            Word(
                *self.conn.execute(
                    "SELECT * FROM word WHERE wordid = ?", (sense.wordid,)
                ).fetchone()
            )
            for sense in senses
        ]
        return words

    def get_synsetdef_by_synset(self, synset: Synset) -> list[Synsetdef]:
        """
        synset => synset_def
        """
        return [
            Synsetdef(*synset_def)
            for synset_def in self.conn.execute(
                'SELECT * FROM synset_def WHERE synset = ? AND lang = "jpn"',
                (synset.synset,),
            ).fetchall()
        ]

    def get_linking_synset(self, synset: Synset) -> list[Synlink]:
        """
        synset => synlink
        """
        return [
            Synlink(*synlink)
            for synlink in self.conn.execute(
                "SELECT * FROM synlink WHERE synset1 = ?", (synset.synset,)
            ).fetchall()
        ]

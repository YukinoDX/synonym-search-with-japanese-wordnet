from flask import Flask, render_template, request
from wordnet import WordNet

app = Flask(__name__)
wn = WordNet()
# TODO: グローバルな定義でいいの？


@app.get("/synonym")
def return_synonym():
    lemma = request.args.get("lemma", "")
    synsets = wn.get_synset_by_lemma(lemma)
    def2lemmas = dict()
    for synset in synsets:
        synsetdefs = wn.get_synsetdef_by_synset(synset)
        words = wn.get_words_by_synset(synset)
        defs = tuple(map(lambda synsetdef: synsetdef.def_, synsetdefs))
        lemmas = [word.lemma for word in words if word.lang == "jpn"]
        def2lemmas[defs] = lemmas

    return render_template("synonym.html", lemma=lemma, def2lemmas=def2lemmas)


@app.get("/links")
def return_links():
    lemma = request.args.get("lemma", "")
    synsets = wn.get_synset_by_lemma(lemma)
    defs2links2lemmas = dict()
    for synset in synsets:
        synsetdef = wn.get_synsetdef_by_synset(synset)
        synlinks = wn.get_linking_synset(synset)
        defs = tuple(map(lambda synsetdef: synsetdef.def_, synsetdef))
        links2lemmas = dict()
        for synlink in synlinks:
            synset2 = wn.get_synset_by_id(synlink.synset2)
            synsetdef2 = wn.get_synsetdef_by_synset(synset2)

            link = (
                synlink.link,
                tuple(map(lambda synsetdef: synsetdef.def_, synsetdef2)),
            )
            lemmas = [
                word.lemma
                for word in wn.get_words_by_synset(synset2)
                if word.lang == "jpn"
            ]
            links2lemmas[link] = lemmas

        defs2links2lemmas[defs] = links2lemmas

    return render_template(
        "links.html", lemma=lemma, defs2links2lemmas=defs2links2lemmas
    )


@app.route("/")
def index():
    return render_template("base.html", lemma="")


if __name__ == "__main__":
    app.run(port=8081)

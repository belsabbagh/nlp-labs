import nltk
import re
import json

nltk_dependencies = ["brown", "stopwords", "punkt", "averaged_perceptron_tagger", "wordnet"]


def download_dependencies():
    for dependency in nltk_dependencies:
        nltk.download(dependency)


def split_into_words(text: str) -> list:
    return re.split(r"\s", text)


def split_into_sentences(text: str) -> list:
    return re.split(r"[.!?][\s\n]", text)


corpus = nltk.corpus.brown


def parse_text(text: str) -> dict:
    text = text.lower()
    words = nltk.word_tokenize(re.sub(r"[^\w\s]", "", text))
    filtered_words = [
        word
        for word in words
        if word not in nltk.corpus.stopwords.words("english")
    ]
    sentences = nltk.sent_tokenize(text)
    frequencies = nltk.FreqDist(filtered_words)
    stemmer = nltk.PorterStemmer()
    stems_dict = {}
    for word in filtered_words:
        stem = stemmer.stem(word)
        if stem in stems_dict:
            stems_dict[stem].append(word)
        else:
            stems_dict[stem] = [word]
    
    lemmatizer = nltk.WordNetLemmatizer()
    lemmas_dict = {}
    for word in filtered_words:
        lemma = lemmatizer.lemmatize(word)
        if lemma in lemmas_dict:
            lemmas_dict[lemma].add(word)
        else:
            lemmas_dict[lemma] = {word}
            
    return {
        "clean_text": " ".join(sentences),
        "most_common_words": dict(frequencies.most_common(10)),
        "sentences": sentences,
        "stems": {stem: list(dervs) for stem, dervs in stems_dict.items()},
        "lemmas": {lemma: list(dervs) for lemma, dervs in lemmas_dict.items()},
    }


if __name__ == "__main__":
    download_dependencies()
    output = {}
    with open("data/sample.md", "r", encoding="utf-8") as f:
        text = f.read()
    output = parse_text(text)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

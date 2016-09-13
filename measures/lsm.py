import statistics

from .liwc import LIWC_DATA


FUNCTION_CLASSES = {'ADP', 'AUX', 'CONJ', 'DET', 'INTJ', 'NUM', 'PART', 'PRON', 'SCONJ'}


def lsm(doc):
    doc_length = len(doc)
    function_words = {function_class: 0 for function_class in FUNCTION_CLASSES}
    for token in doc:
        if token.pos_ in FUNCTION_CLASSES:
            function_words[token.pos_] += 1

    return {word_class: (count / doc_length) * 100 for word_class, count in function_words.items()}


def liwc_lsm(doc):
    function_words = {function_class: 0 for function_class in LIWC_DATA}
    for word in doc:
        word = word.lower()
        for function_class in LIWC_DATA:
            for function_word in function_class:
                if function_word.endswith('*'):
                    if word.startswith(function_word[:-1]):
                        function_words[function_class] += 1
                else:
                    if word == function_word:
                        function_words[function_class] += 1

    return {word_class: (count / len(doc)) * 100 for word_class, count in function_words.items()}


def dyad_lsm(doc1, doc2, lsm_func=lsm):
    lsm1 = lsm_func(doc1)
    lsm2 = lsm_func(doc2)
    scores = []

    if lsm_func == liwc_lsm:
        classes = LIWC_DATA
    else:
        classes = FUNCTION_CLASSES

    for word_class in classes:
        scores.append(1 - abs(lsm1[word_class] - lsm2[word_class]) / (lsm1[word_class] + lsm2[word_class] + .0001))

    return statistics.mean(scores)

import statistics


FUNCTION_CLASSES = {'ADP', 'AUX', 'CONJ', 'DET', 'INTJ', 'NUM', 'PART', 'PRON', 'SCONJ'}


def lsm(doc):
    doc_length = len(doc)
    function_words = {function_class: 0 for function_class in FUNCTION_CLASSES}
    for token in doc:
        if token.pos_ in FUNCTION_CLASSES:
            function_words[token.pos_] += 1

    return {word_class: (count / doc_length) * 100 for word_class, count in function_words.items()}


def dyad_lsm(doc1, doc2):
    lsm1 = lsm(doc1)
    lsm2 = lsm(doc2)
    scores = []
    for word_class in FUNCTION_CLASSES:
        scores.append(1 - abs(lsm1[word_class] - lsm2[word_class]) / (lsm1[word_class] + lsm2[word_class] + .0001))

    return statistics.mean(scores)

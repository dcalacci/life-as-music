from collections import defaultdict
import lexicons.lexiconUtils as lexiconUtils
import itertools

liwc_dict = lexiconUtils.LiwcDict()


def sentiment_dict_words(sen):
    """produces list of words in sen that exist in sentiment_dict.
    """
    return [word for word in sen if liwc_dict.exists(word)]


def is_negated(sen, index):
    """returns True if the word at index is negated in sen.
    """
    def get_previous_words(sen, index):
        index_range = range(index - 3, index)
        return [r for r in index_range if r >= 0]

    def is_negation(w):
        return liwc_dict.isNegation(w)

    prev_words = get_previous_words(sen, index)
    negations = [is_negation(sen[i]) for i in prev_words]
    return any(negations)


def get_categories_for_word(sen, index):
    """returns a list of categories that the word at the given index
    belongs to.
    """
    word = sen[index]
    if liwc_dict.exists(word):
        categories = liwc_dict.getCategories(word)

        # if the word is negated and has + or - sentiment, replace
        # any categories that have opposites
        if (
                (liwc_dict.isPosWord(sen[index]) or
                 liwc_dict.isNegWord(word)) and
                is_negated(sen, index)
        ):

            def replaceCategory(c):
                opposite = liwc_dict.getOppositeCategory(c)
                if opposite:
                    return opposite
                else:
                    return c

            categories = map(replaceCategory, categories)
        return categories
    return []


def _is_neg_word(sen, index):
    """
    Checks if the word at index should be counted as negative in 'sen'
    """
    categories = get_categories_for_word(sen, index)
    if categories:
        return any(map(liwc_dict.isNegCat, categories))
    else:
        return False


def _is_pos_word(sen, word):
    """
    Checks if the word at index should be counted as positive in 'sen'
    """
    categories = get_categories_for_word(sen, word)
    if categories:
        return any(map(liwc_dict.isPosCat, categories))
    else:
        return False


def _normalize(feature_vector, word_count):
    """
    Normalizes the given feature vector's values by word_count.
    """
    for feature, score in feature_vector.items():
        feature_vector[feature] = score/float(word_count)
    return feature_vector


def pos_neg_classify_sentence(sen):
    """
    creates a classification vector for a particular sentence,
    using positive and negative categories as features.
    The value for each feature is normalized by the size of the
    sentence itself. Ignores entities.

    @type  sen: sentence
    @param sen: The sentence to analyze

    @rtype dict
    @return: a feature vector of [feature] -> [value]
    """
    pos_neg_vector = {}
    pos_neg_vector["pos"] = 0
    pos_neg_vector["neg"] = 0

    for index in range(len(sen)):
        if _is_pos_word(sen, index):
            pos_neg_vector["pos"] += 1
        elif _is_neg_word(sen, index):
            pos_neg_vector["neg"] += 1
    return _normalize(pos_neg_vector, len(sen))


def get_liwc_vector_for_words(words, categories=liwc_dict.categories):
    feature_vector = dict(zip(categories, [0] * len(categories)))
    #feature_vector = defaultdict(int)
    sen_categories = [get_categories_for_word(words, i) for i in range(len(words))]

    # flatten list
    sen_categories = itertools.chain(*sen_categories)
    sen_categories = [c for c in sen_categories if c in categories]
    for c in sen_categories:
        feature_vector[c] += 1
    return _normalize(feature_vector, len(words))

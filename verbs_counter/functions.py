from nltk import pos_tag, download

VERB_TAGS = ('VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ')


def flat_list(_list):
    """ [(1,2), (3,4)] -> [1, 2, 3, 4]"""
    return sum([list(item) for item in _list], [])


def is_verb(word):
    if not word:
        return False
    try:
        pos_info = pos_tag([word])
    except LookupError:
        download('averaged_perceptron_tagger')
        pos_info = pos_tag([word])
    return pos_info[0][1] in VERB_TAGS


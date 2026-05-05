import re


rxWord = re.compile('[^ ]+')


def process_simple_query(query, sc):
    """
    Read an HTML query encoded as a dictionary, which comes from the
    simple interface. Modify, add or delete keys or values. Note that
    most keys consist of a field ID concatenated with a query word number,
    e.g., lex1 for "the lemma of the first query word". This does not include
    fields that are only relevant for the query as a whole, e.g., n_words
    or document-level metadata fields.
    This function MUST BE WRITTEN FROM SCRATCH if you want to use it in your
    corpus. You must tailor it to your needs. What you see here is just a stub.
    The only relevant field here is all_in_one_search_txt. It contains a prompt
    entered by the user. It has to be parsed however you like, e.g., by splitting
    it into words and turning them into lemma queries. You can also add metadata
    values in order to search in a particular subcorpus.
    Note that n_words equals -1 (an indication that a simple search has been
    invoked). In the resulting query, n_words has to be greater than 0.
    You can use the SearchClient object (sc) to check if a word or a lemma
    exists in the database (sc.word_exists) and use this information when
    building your query.
    """
    query['n_words'] = 1
    txt = query['all_in_one_search_txt'].strip()
    del query['all_in_one_search_txt']
    query['precise'] = 'on'

    words = rxWord.findall(txt)
    if 'lang1' not in query or len(query['lang1']) > 0:
        query['lang1'] = sc.settings.languages[0]
    if len(words) > 1:
        query['txt'] = txt
        query['wf1'] = ''
        query['lex1'] = ''
    elif len(words) == 1:
        if txt.startswith('[') and txt.endswith(']'):
            # Lemma request
            query['wf1'] = ''
            query['lex1'] = txt.strip('[]')
        elif txt.startswith('"') and txt.endswith('"'):
            # Word request
            query['wf1'] = txt.strip('"')
            query['lex1'] = ''
        elif sc.word_exists(txt, 'lex', lang=query['lang1']):
            query['wf1'] = ''
            query['lex1'] = txt
        else:
            query['wf1'] = txt
            query['lex1'] = ''

    return query

import unicodedata


def make_uri(s):
    """
    This method is used to clean an string and convert it to uri
    :param s: A string to be cleaned
    :return: The string as uri
    """
    s = s.replace(" ", "")
    s = ''.join(e for e in s if e.isalnum())
    s = ''.join([i for i in s if not i.isdigit()])
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                   if unicodedata.category(c) != 'Mn')

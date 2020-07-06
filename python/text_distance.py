
import textdistance

# test buffers
l = [
    'Kamaci', '#admin', '#Admin', 'weechat', 'freenode', '#gomuks',
    'Aditya', 'javbit', '#python', '#python', '##linux', 'NickServ',
    '#ECE445', 'chin123', '#weechat', '#weechat', '#helpdesk', '#fread.ink',
    '#PurdueLUG', '#uiuclug', 'matrix_org', 'BASHy2-EU', '#reMarkable', '#pykeepass',
    '#Zerophone', '#keepassxc', '#t2bot.io', 'irc.sdf.org', 'evidlo_test',
    '#gpu-cluster', '#test_invite', 'johnwidloski', '#System Alerts', '#Matrix Bridging',
    '#IRC Matrix Bridges', '@swidlo77:matrix.org', '#Matrix Puppet Bridge', '@markwidloski:matrix.org',
    '@appservice-irc:matrix.org', '#This Week in Matrix (TWIM)', '#lumos (PM on chat.freenode.net)',
    '#Eeems (PM on chat.freenode.net)', '#[Discord] Meme lounge #meme-lounge',
    '#evidlo2 (PM on chat.freenode.net)', '#NickServ (PM on chat.freenode.net)',
    '#NickServ (PM on chat.freenode.net)', '#NickServ (PM on chat.freenode.net)',
    '#ChanServ (PM on chat.freenode.net)', '#freenode-connect (PM on chat.freenode.net)',
    'slack.wee-slack-test.#random'
]


def jw(s1, s2):

    s1_len = len(s1)
    s2_len = len(s2)

    if not s1_len or not s2_len:
        return 0.0

    min_len = max(s1_len, s2_len)
    search_range = (min_len // 2) - 1
    if search_range < 0:
        search_range = 0

    s1_flags = [False] * s1_len
    s2_flags = [False] * s2_len

    # looking only within search range, count & flag matched pairs
    common_chars = 0
    for i, s1_ch in enumerate(s1):
        low = max(0, i - search_range)
        hi = min(i + search_range, s2_len - 1)
        for j in range(low, hi + 1):
            if not s2_flags[j] and s2[j] == s1_ch:
                s1_flags[i] = s2_flags[j] = True
                common_chars += 1
                break

    # short circuit if no characters match
    if not common_chars:
        return 0.0

    # count transpositions
    k = trans_count = 0
    for i, s1_f in enumerate(s1_flags):
        if s1_f:
            for j in range(k, s2_len):
                if s2_flags[j]:
                    k = j + 1
                    break
            if s1[i] != s2[j]:
                trans_count += 1
    trans_count //= 2

    # adjust for similarities in nonmatched characters
    weight = common_chars / s1_len + common_chars / s2_len
    weight += (common_chars - trans_count) / common_chars
    return -weight

def go_match_fuzzy(name, string):
    """Check if string matches name using approximation."""
    if not string:
        return False

    name_len = len(name)
    string_len = len(string)

    if string_len > name_len:
        return False
    if name_len == string_len:
        return name == string

    # Attempt to match all chars somewhere in name
    prev_index = -1
    for i, char in enumerate(string):
        index = name.find(char, prev_index+1)
        if index == -1:
            return False
        prev_index = index
    return True


def _pure_python(s1, s2):
    """
    https://www.guyrutenberg.com/2008/12/15/damerau-levenshtein-distance-in-python/
    """
    d = {}

    # matrix
    for i in range(-1, len(s1) + 1):
        d[i, -1] = i + 1
    for j in range(-1, len(s2) + 1):
        d[-1, j] = j + 1

    for i, cs1 in enumerate(s1):
        for j, cs2 in enumerate(s2):
            cost = int(cs1 != cs2)
            # ^ 0 if equal, 1 otherwise

            d[i, j] = min(
                d[i - 1, j] + 1,            # deletion
                d[i, j - 1] + 1,            # insertion
                d[i - 1, j - 1] + cost,     # substitution
            )

            # transposition
            if not i or not j:
                continue
            if cs1 != s2[j - 1]:
                continue
            if s1[i - 1] != cs2:
                continue
            d[i, j] = min(
                d[i, j],
                d[i - 2, j - 2] + cost,
            )

    return 100 - d[len(s1) - 1, len(s2) - 1]

def damerau_levenshtein_distance_improved(a, b):
    # "Infinity" -- greater than maximum possible edit distance
    # Used to prevent transpositions for first characters
    INF = len(a) + len(b)

    # Matrix: (M + 2) x (N + 2)
    matrix  = [[INF for n in range(len(b) + 2)]]
    matrix += [[INF] + list(range(len(b) + 1))]
    matrix += [[INF, m] + [0] * len(b) for m in range(1, len(a) + 1)]

    # Holds last row each element was encountered: DA in the Wikipedia pseudocode
    last_row = {}

    # Fill in costs
    for row in range(1, len(a) + 1):
        # Current character in a
        ch_a = a[row-1]

        # Column of last match on this row: DB in pseudocode
        last_match_col = 0

        for col in range(1, len(b) + 1):
            # Current character in b
            ch_b = b[col-1]

            # Last row with matching character
            last_matching_row = last_row.get(ch_b, 0)

            # Cost of substitution
            cost = 0 if ch_a == ch_b else 1

            # Compute substring distance
            matrix[row+1][col+1] = min(
                matrix[row][col] + cost, # Substitution
                matrix[row+1][col] + 1,  # Addition
                matrix[row][col+1] + 1,  # Deletion

                # Transposition
                # Start by reverting to cost before transposition
                matrix[last_matching_row][last_match_col]
                    # Cost of letters between transposed letters
                    # 1 addition + 1 deletion = 1 substitution
                    + max((row - last_matching_row - 1),
                          (col - last_match_col - 1))
                    # Cost of the transposition itself
                    + 1)

            # If there was a match, update last_match_col
            if cost == 0:
                last_match_col = col

        # Update last row for current character
        last_row[ch_a] = row

    # Return last element
    return 100 - matrix[-1][-1]

class DL1(object):
    def normalized_distance(self, a, b):
        return damerau_levenshtein_distance_improved(a, b)
class DL2(object):
    def normalized_distance(self, a, b):
        return go_match_fuzzy(a, b)
class DL3(object):
    def normalized_distance(self, a, b):
        return jw(a, b)

textdistance.dl1 = DL1()
textdistance.dl2 = DL2()
textdistance.dl3 = DL3()

# algorithms to test

# algs = ['hamming', 'mlipns', 'levenshtein', 'damerau_levenshtein', 'jaro',
#         'strcmp95', 'needleman_wunsch', 'smith_waterman', 'jaccard', 'sorensen',
#         'tversky', 'overlap', 'cosine', 'monge_elkan', 'bag', 'dl']
algs = ['levenshtein', 'damerau_levenshtein', 'jaro',
        'strcmp95', 'jaccard', 'sorensen',
        'tversky', 'bag', 'dl1', 'dl2', 'dl3']

def query(string, limit=5):
    # return top 5 results for all algorithms
    for alg in algs:
        func = getattr(textdistance, alg)
        result = list(sorted(l, key=lambda x:func.normalized_distance(string.lower(), x.lower())))[:limit]
        print(f"{alg}:", result)

def plot(string, presort=True):
    if presort:
        sort = list(sorted(l, key=lambda x:textdistance.damerau_levenshtein.normalized_distance(string, x)))
    else:
        sort = l
    import matplotlib.pyplot as plt
    for alg in algs:
        func = getattr(textdistance, alg)
        scores = []
        for x in sort:
            scores.append(func.normalized_distance(string, x))
        plt.plot(scores, label=alg)
        plt.legend()

query('weer')

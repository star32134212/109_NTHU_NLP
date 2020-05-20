from collections import defaultdict


def estimate_tef_and_tfe(ef_tokens, ef_alignments):
    token_pair_set = set()
    total_ef = defaultdict(lambda: defaultdict(lambda: 0))
    total_e = defaultdict(lambda: 0)
    total_f = defaultdict(lambda: 0)
    t_ef = defaultdict(lambda: defaultdict(lambda: 0))
    t_fe = defaultdict(lambda: defaultdict(lambda: 0))
    for (e_tokens, f_tokens), alg_of_sent in zip(ef_tokens, ef_alignments):
        idx_alg = [alg.split('-') for alg in alg_of_sent.split(' ')]
        word_alg = idx_alg_to_word_alg(e_tokens, f_tokens, idx_alg)
        for e, f in word_alg:
            total_e[e] += 1
            total_f[f] += 1
            total_ef[e][f] += 1
            token_pair_set.add((e, f))
    for e, f in token_pair_set:
        t_ef[e][f] = total_ef[e][f] / total_f[f]
        t_fe[f][e] = total_ef[e][f] / total_e[e]
    return (t_ef, t_fe)


def idx_alg_to_word_alg(e_tokens, f_tokens, idx_alg):
    e_idx_list = [int(e_idx) for e_idx, _ in idx_alg]
    f_idx_list = [int(f_idx) for _, f_idx in idx_alg]
    word_alg = [(e_tokens[e_idx], f_tokens[f_idx])
                for e_idx, f_idx in zip(e_idx_list, f_idx_list)]
    for e_idx, e in enumerate(e_tokens):
        if e_idx not in e_idx_list:
            word_alg.append((e, '[NULL]'))
    for f_idx, f in enumerate(f_tokens):
        if f_idx not in f_idx_list:
            word_alg.append(('[NULL]', f))
    return word_alg
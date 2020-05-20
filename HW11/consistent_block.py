def extract(f_start, f_end, e_start, e_end, 
            alignment, e_aligned, f_aligned,
            srctext, trgtext, srclen, trglen):
    if f_end < 0:  # 0-based indexing.
        return {}
    for e,f in alignment:
        if ((f_start <= f <= f_end) and
           (e < e_start or e > e_end)):
            return {}

    phrases = set()
    fs = f_start
    while True:
        fe = f_end
        while True:
            src_phrase = " ".join(srctext[i] for i in 
                                  range(e_start,e_end+1))
            trg_phrase = " ".join(trgtext[i] for i in range(fs,fe+1))
            # print(src_phrase)
            # print(trg_phrase)
            # print()
            phrases.add((e_start, e_end+1, fs, fe+1,))
            fe += 1
            if fe in f_aligned or fe == trglen:
                break
        fs -=1 
        if fs in f_aligned or fs < 0:
            break
    return phrases

def phrase_extraction(srctext, trgtext, alignment):
    srclen = len(srctext)       # len(e)
    trglen = len(trgtext)       # len(f)
    # Keeps an index of which source/target words that are aligned.
    e_aligned = [i for i,_ in alignment]
    f_aligned = [j for _,j in alignment]

    bp = set() # set of phrase pairs BP
    for e_start in range(srclen):
        for e_end in range(e_start, srclen):
            f_start, f_end = trglen-1 , -1  #  0-based indexing
            for e,f in alignment:
                if e_start <= e <= e_end:
                    f_start = min(f, f_start)
                    f_end = max(f, f_end)
            phrases = extract(f_start, f_end, e_start, e_end, 
                              alignment, e_aligned, f_aligned,
                              srctext, trgtext, srclen, trglen)
            if phrases:
                bp.update(phrases)
    return bp

if __name__ == "__main__":
    source = "michael assumes that he will stay in the house".split()
    target = "michael geht davon aus , dass er im haus bleibt".split()
    alignment = [(0,0), (1,1), (1,2), (1,3), (2,5), (3,6), (4,9), (5,9), (6,7), (7,7), (8,8)]

    # print(phrase_extraction(source, target, alignment))
    for e_start, e_end, fs, fe in sorted(phrase_extraction(source, target, alignment)):
        print(e_start, e_end)
        print(" ".join(source[e_start:e_end]))
        print(fs, fe)
        print(" ".join(target[fs:fe]))
        print()

def next_target(opt, slist):
    indexes = []
    target_names = list(s.target for s in slist)
    for t in opt.targets:
        try:
            i = int(t)
        except ValueError:
            i = target_names.index(t)
        indexes.append(i)

    if hasattr(opt, 'inverse') and opt.inverse:
        indexes = list(i for i in range(len(slist)) if i not in indexes)

    for i in indexes or range(len(slist)): yield i, slist[i]

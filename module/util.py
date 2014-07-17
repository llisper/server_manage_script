def next_target(opt, slist):
    indexes = opt.target_indexes[:]
    target_names = list(s.target for s in slist)
    for t in opt.targets:
        i = target_names.index(t)
        if i not in indexes:
            indexes.append(i)
    for i in indexes or range(len(slist)): yield i, slist[i]

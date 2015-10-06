
blockChar = '^'

def tokenizer():
    pass

def caParser(target, master):
    targetIter = target.__iter__()
    masterIter = master.__iter__()
    while True:
        try:
            tChar = next(targetIter)
        except StopIteration:
            break
        try:
            mChar = next(masterIter)
        except StopIteration:
            raise Exception("Master is shorter than target.")
        if tChar == mChar:
            pass
        else:
            print("{} | {}".format(tChar, mChar))

def fileParse(target, master):
    print(target)
    with open(target) as fTarget:
        with open(master) as fMaster:
            caParser(fTarget.read(),fMaster.read())

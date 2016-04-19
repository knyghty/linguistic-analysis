def subtrees(doc):
    deps = []
    for word in doc:
        children = list(word.children)
        if len(children):
            deps.append((word.dep, [child.dep for child in children]))
    return deps

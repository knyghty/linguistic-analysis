def remove_whitespace(doc):
    """Return a list of non-whitespace tokens in doc."""
    return [token for token in doc if token.string.strip()]

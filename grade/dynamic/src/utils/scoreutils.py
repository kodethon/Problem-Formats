def score_map(score, max_score=None, comment=''):
    if max_score is None:
        max_score = score
    return {'score':score,
            'max_score':max_score,
            'output':comment}
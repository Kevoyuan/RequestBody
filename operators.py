# operators.py

operators = [
    # 'or' operator
    (['\bor\b', 'one of'], '/'),
    
    # 'and' operator
    (['and'], '+'),
    
    # 'not' operator
    (['without', 'not including', 'excluding'], '-'),
    
    # 'and not' operator
    (['except'], '+-'),
    
    # 'or not' operator
    (['\bor .*? without\b'], '/-')
]

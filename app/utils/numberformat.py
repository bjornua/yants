# -*- coding: utf-8 -*-

si_units = (
    ("deca" , 1e1 ),
    ("hecto", 1e2 ),
    ("kilo" , 1e3 ),
    ("mega" , 1e6 ),
    ("giga" , 1e9 ),
    ("tera" , 1e12),
    ("peta" , 1e15),
    ("exa"  , 1e18),
    ("zetta", 1e21),
    ("yotta", 1e24)
)

def format_size(number):
    prev = si_units[0]
    
    if number < prev[1]:
        return "%i bytes" % (number,)

    for x in si_units[1:]:
        if number < x[1]:
            break
        prev = x
         
    number /= prev[1]

    return "%.1f %s" % (number, prev[0])

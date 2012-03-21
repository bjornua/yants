# -*- coding: utf-8 -*-

_config = None

def get():
    global _config
    
    if _config != None:
        return _config

    import app.config.default as dconfig
    
    _config = dict(dconfig.config)

    try:
        import app.config.user as uconfig
    except ImportError:
        pass
    else:
        _config.update(uconfig.config)

    return _config


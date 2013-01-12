#coding=UTF-8

from unicodedata import normalize
from string import punctuation

def remover_acentos(txt, codif='utf-8'):
    ''' 
    Returns a copy of replacing the characters str
    accentuated by their not accented equivalents.
    
      WARNING: graphics not ASCII characters and non-alphanumeric,
      such as bullets, dashes, quotation marks, asymmetric, etc..
      are simply removed!
    
    '''
    
    try:
        return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')
    except Exception:
        #request.print_logging('Remove Acentos: ' + txt)
        return None

texto = u"@faithsone ㅋㅋㅋ u so smart & progressive. i thou'ght u were like @moontoseu or rick santorum ^^;"

print remover_acentos(texto, "utf-8")

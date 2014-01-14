from base64 import b64decode


def b64str_to_hexstr (b64str):
    bytestr = b64decode (b64str, '-~')
    return bytestr.encode('hex')


def hexstr_to_int (hexstr):
    return int (hexstr, 16)


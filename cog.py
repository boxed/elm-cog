# Fake cog module for testing

_result = None


def out(s):
    _result.append(s)


def outl(s):
    _result.append(s)
    _result.append('\n')


def reset():
    global _result
    _result = []


def result():
    global _result
    r = ''.join(_result)
    _result = None
    return r

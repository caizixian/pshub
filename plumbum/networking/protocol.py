"""
sub \t rule ... \r\n
pub \t Message ... \r\n
rep \t reply ... \r\n
"""
#!/usr/bin/env python3
import json
def make_body(obj): 
    return json.dumps(obj) 

def parse_body(string): 
    return json.loads(string)

def make_message(ty, obj):
    types = {
        'sub': lambda x: 'sub\t' + make_body(x),
        'pub': lambda x: 'pub\t' + make_body(x),
        'rep': lambda x: 'rep\t' + make_body(x)
    }
    return types[ty](obj)

def make_result(string):
    ty, body = string.split('\t')
    return ty, parse_body(body)

def parse_message(string, rest):
    rest += string
    result = []
    rest_list = rest.split('\r\n')
    for x in rest_list[:-1]:
        result.append(make_result(x))
    return result, rest_list[-1]
"""
def main():
    a = {'level': 5, 'sum': 7}
    c = {'level': 7}
    sa = make_message('pub', a)
    sc = make_message('sub', c)
    sa += '\r\n'
    sa += sc[:-2]
    sc = sc[-2:] + '\r\n'
    res, rest = parse_message(sa, '')
    print(res)
    print(rest)
    res, rest = parse_message(sc, rest)
    print(res)
    print(rest)

if __name__ == '__main__':
    main()
"""
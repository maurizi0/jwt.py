#!/usr/bin/env python3
import sys
import base64
import json

class JwtUtils:
    # Add padding to a base64 string if needed
    def pad(self, b64):
        alignment = len(b64) % 4
        if alignment == 2:
            b64 += '=='
        elif alignment == 3:
            b64 += '='
        return b64

    def print_jwt(self, jwt_arr, pretty=False):
        header = jwt_arr[0]
        claims = jwt_arr[1]
        signature = jwt_arr[2]

        if (pretty):
            header = json.loads(header)
            header = json.dumps(header, indent=4, sort_keys=True)
            claims = json.loads(claims)
            claims = json.dumps(claims, indent=4, sort_keys=True)

        print('{}.{}.{}'.format(header, claims, signature))

    def decode_jwt(self, jwt_arr):
        header = base64.urlsafe_b64decode(self.pad(jwt_arr[0])).decode('utf-8')
        claims = base64.urlsafe_b64decode(self.pad(jwt_arr[1])).decode('utf-8')
        signature = str(jwt_arr[2])
        return [header, claims, signature]

    def encode_jwt(self, jwt_arr):
        header = base64.urlsafe_b64encode(jwt_arr[0]).decode('utf-8').strip('=')
        claims = base64.urlsafe_b64encode(jwt_arr[1]).decode('utf-8').strip('=')
        signature = jwt_arr[2].decode('utf-8')
        return [header, claims, signature]

class Cli:
    PRETTY = '--pretty'
    DECODE = '-d'
    ENCODE = '-e'
    HELP   = '-h'

    def __init__(self):
        self.decode = True
        self.pretty = False
        self.raw_jwt_arr = []
        self.parse_argv()

    def parse_argv(self):
        if (self.HELP in sys.argv):
            self.usage()
            sys.exit()
        if (self.PRETTY in sys.argv):
            self.pretty = True
        if (self.ENCODE in sys.argv):
            self.decode = False

        if sys.stdin.isatty():
            print('ERROR: stdin empty')
            sys.exit(1)

        if self.decode:
            for line in sys.stdin:
                self.raw_jwt_arr = line.rstrip().split('.')
        else:
            for line in sys.stdin:
                self.raw_jwt_arr = line.rstrip().split('}.')
                self.raw_jwt_arr[0] = (self.raw_jwt_arr[0] + '}').encode('utf-8')
                self.raw_jwt_arr[1] = (self.raw_jwt_arr[1] + '}').encode('utf-8')
                self.raw_jwt_arr[2] = self.raw_jwt_arr[2].encode('utf-8')

        if len(self.raw_jwt_arr) != 3:
            print('ERROR: invalid jwt format')
            sys.exit(1)

    def usage(self):
        print('usage: jwt {} | {} | {} | ({})'.format(self.DECODE, self.ENCODE, self.HELP, self.PRETTY))
        print('{}           decode stdin'.format(self.DECODE))
        print('{}           encode stdin'.format(self.ENCODE))
        print('{}           help'.format(self.HELP))
        print('{}     pretty print output'.format(self.PRETTY))


def main():
        cli = Cli();
        jwtUtils = JwtUtils()
        
        if (cli.decode):
            jwt_arr = jwtUtils.decode_jwt(cli.raw_jwt_arr)
            jwtUtils.print_jwt(jwt_arr, cli.pretty)
        else:
            jwt_arr = jwtUtils.encode_jwt(cli.raw_jwt_arr)
            jwtUtils.print_jwt(jwt_arr)

main()



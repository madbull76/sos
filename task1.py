#!/usr/bin/env python3

import sys
import json
import argparse

REQUIRED = 'domain_name'

def main(data):
    
    try:
        json_loaded = json.loads(data)
        if json_loaded:
            for item in json_loaded:
                if item.get(REQUIRED):

                    if item.get('disabled'):
                        continue
                    
                    if item.get('username') and item.get('password'):
                        auth = '{}:{}@'.format(item.get('username'), item.get('password'))
                    elif item.get('username') and not item.get('password'):
                        auth = '{}@'.format(item.get('username'))
                    else:
                        auth = ''


                    if item.get('query'):
                        if len(item.get('query')) != 0:
                            query_string = str()
                            for q in item.get('query').items():
                                query_string +='&{}={}'.format(q[0],q[1])
                            query_string = query_string[1:]
                            query_string = '?{}'.format(query_string[:-1])
                    else:
                        query_string = ''

                    sys.stdout.write('{schema}://{auth}{domain_name}{port}/{path}{query}{fragment}\n\r'.format(
                                                        schema=item.get('scheme'),
                                                        domain_name=item.get('domain_name'),
                                                        port=':{}'.format(item.get('port')) if item.get('port') else '',
                                                        path=item.get('path') if item.get('path') else '',
                                                        fragment='#{}'.format(item.get('fragment')) if item.get('fragment') else '',
                                                        auth=auth,
                                                        query=query_string
                                                        ))
                
        else:
            sys.stderr.write("No data found to decode. Exiting...")
            return
    except ValueError:
        sys.stderr.write("Decoding JSON failed.")
        return

    return    


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('infile',
                    default=sys.stdin,
                    type=argparse.FileType('r', encoding='utf-8'),
                    nargs='?')

    args = parser.parse_args()

    main(args.infile.read())
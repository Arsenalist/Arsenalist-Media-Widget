import json, os, argparse
from jinja2 import Template
from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods.posts import GetPosts

def create_file(file_name, file_content):
    f = open(file_name, 'wb')
    f.write(file_content)
    f.close()


def read_file(file):
    with open(file, 'r') as content_file:
        content = content_file.read()
    return content


def create_embed(posts):
    info = {'bits': posts}
    template = Template(read_file('template.html'))
    return template.render(info)



def main():
    p = argparse.ArgumentParser(description='Create an embeddable page for Arsenalist videos')
    p.add_argument('-u', '--username', required=True)
    p.add_argument('-p', '--password', required=True)
    args = vars(p.parse_args())
    username = args['username']
    password = args['password']

    wp = Client('https://arsenalist.com/xmlrpc.php', username, password)
    posts = wp.call(GetPosts())
    bits = []
    for p in posts:
        custom_fields = p.custom_fields
        for cf in custom_fields:
            if cf['key'] == 'gallery_json':
                raw = json.loads(cf['value'])
                raw = raw[::-1]
                for r in raw:
                    if 'sort' not in r: 
                        r['sort'] = 0
                raw = sorted(raw, key=lambda item: item['sort'], reverse=True)
                bits.extend(raw)

    print(create_embed(bits))

if __name__ == '__main__':
    main()


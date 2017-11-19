import os
import re
from console_logging.console import Console
console = Console()


def parse_blog(blogdat: list):
    blog = dict()
    blog['title'] = blogdat[0][:-1]

    def parse_timestamp(timestamp: str):
        date, time = timestamp.split(' ')
        month, day, year = date.split('/')
        hours, minutes = time.split(':')
        date = dict()
        time = dict()
        date['m'] = month
        date['d'] = day
        date['y'] = year
        time['h'] = hours
        time['m'] = minutes
        return {'date': date, 'time': time}
    blog['timestamp'] = parse_timestamp(blogdat[1][:-1])
    blog['tags'] = re.sub(' ', '', blogdat[2][:-1]).lower().split(',')
    blog['nsfw'] = 'nsfw' in blog['tags']
    blog['body'] = [line.replace('\n', '') for line in blogdat[4:]]
    return blog


def render_blog(blog: dict):
    title = '<h1>%s <small>%s</small></h1>' % (
        blog['title'], ('(NSFW)' if blog['nsfw'] else ''))
    date = blog['timestamp']['date']
    time = blog['timestamp']['time']
    timestamp = '%s/%s/%s || %s:%s' % (date['m'],
                                       date['d'],
                                       date['y'],
                                       time['h'],
                                       time['m'])

    def render_body(body: list):
        body_ = []
        for line in body:
            if '-' in line and len(line.replace('-', '')) == 0:
                body_.append('<hr>')
            elif line == '~':
                body_.append('<hr>')  # TODO: add tilda
            elif len(line)>0 and len(re.sub('(\[).+(\])(\().+(\))', '', line)) == 0:
                alt_text = line[1:line.rfind(']')]
                link = line[line.find('(') + 1:-1]
                body_.append('<img src="{link}" alt="{alt}">'.format(
                    link=link,
                    alt=alt_text))
            else:
                while line.count('*') > 1:
                    print(line)
                    occ1 = line.find('*')
                    occ2 = occ1 + line[occ1 + 1:].find('*') + 1
                    line = '%s<b>%s</b>%s' % (line[:occ1],
                                              line[occ1 + 1:occ2], line[occ2 + 1:])
                while line.count('_') > 1:
                    print(line)
                    occ1 = line.find('_')
                    occ2 = occ1 + line[occ1 + 1:].find('_') + 1
                    line = '%s<i>%s</i>%s' % (line[:occ1],
                                              line[occ1 + 1:occ2], line[occ2 + 1:])
                while line.count('~') > 1:
                    print(line)
                    occ1 = line.find('~')
                    occ2 = occ1 + line[occ1 + 1:].find('~') + 1
                    line = '%s<s>%s</s>%s' % (line[:occ1],
                                              line[occ1 + 1:occ2], line[occ2 + 1:])
                body_.append(line)
        return '\n<br>\n'.join(body_)
    body = render_body(blog['body'])
    return '''<!DOCTYPE html>
    <html>
        {head}
        <body>
            {title}
            {timestamp}
            <br>
            <br>
            {body}            
        </body>
    </html>
    '''.format(head='<head><title>Masquerade Blog</title></head>',
               title=title, timestamp=timestamp,
               body=body)


try:
    os.makedirs('./blog')
except:
    pass

for file in os.listdir('./blogs'):
    ext = file.split('.')[-1]
    if ext == 'blog':
        blog_id = file.split('.')[0]
        with open('./blogs/%s' % file, 'r') as blog_def:
            parsed_blog = parse_blog(blog_def.readlines())
            blog_html = render_blog(parsed_blog)
            with open('./blog/%s.html' % blog_id, 'w') as blog:
                blog.write(blog_html)
        console.info("Wrote blog id::%s" % blog_id)
console.success("Finished blogging.")

# script to download the emoticons from GitHub and to produce a table for
# inclusion in Doxygen. Works with python 2.7+ and python 3.x
import json
import os
import argparse
import re
try:
    import urllib.request as urlrequest
except ImportError:
    import urllib as urlrequest

unicode_re = re.compile(r'.*?/unicode/(.*?).png\?.*')

def get_emojis():
    response  = urlrequest.urlopen('https://api.github.com/emojis')
    raw_data  = response.read()
    return json.loads(raw_data)

def download_images(dir_name, silent):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    json_data = get_emojis()
    num_items = len(json_data)
    cur_item=0
    for image,url in sorted(json_data.items()):
        image_name = image+'.png'
        cur_item=cur_item+1
        if url.find('/unicode/')==-1 or not os.path.isfile(dir_name+'/'+image_name):
            success = True
            with open(dir_name+'/'+image_name,'wb') as file:
                if not silent:
                    print('%s/%s: fetching %s' % (cur_item,num_items,image_name))
                try:
                    file.write(urlrequest.urlopen(url).read())
                except:
                    print('Unable to fetch %s' % (image_name))
                    success = False
            if not success:
                os.remove(dir_name+'/'+image_name)
        else:
            if not silent:
                print('%s/%s: skipping %s' % (cur_item,num_items,image_name))

def produce_table():
    json_data = get_emojis()
    lines = []
    for image,url in sorted(json_data.items()):
        match = unicode_re.match(url)
        if match:
            unicodes = match.group(1).split('-')
            unicodes_html = ''.join(["&#x"+x+";" for x in unicodes])
            image_str = "\":"+image+":\","
            unicode_str = "\""+unicodes_html+"\""
            lines.append('  { %-42s %-38s }' % (image_str,unicode_str))
    out_str = ',\n'.join(lines)
    print("{")
    print(out_str)
    print("};")

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-d','--dir',help='directory to place images in')
    parser.add_argument('-t','--table',help='generate code fragment',action='store_true')
    parser.add_argument('-s','--silent',help='silent mode',action='store_true')
    args = parser.parse_args()

    if args.table:
        produce_table()
    if args.dir:
        download_images(args.dir, args.silent)

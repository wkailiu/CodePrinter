import argparse
import os
import sys
import warnings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--code_folder', type=str)
    parser.add_argument('-f', '--file_types', type=str, default='py,cpp')
    parser.add_argument('-n', '--page_lines', type=int, default=87)
    parser.add_argument('-m', '--max_length', type=int, default=110)
    parser.add_argument('-s', '--style', type=str, default='default.css')
    args = parser.parse_args()
    
    file_type_list = args.file_types.split(',')

    file_list = []
    for folder, _, fn_list in os.walk(args.code_folder):
        for fn in fn_list:
            if fn.split('.')[-1] in file_type_list:
                file_list.append(os.path.join(folder, fn))
    
    file_list.sort()
    # check code length
    check = True
    for fn in file_list:
        with open(fn, 'r') as fr:
            lines = fr.readlines()
        
        for i, line in enumerate(lines):
            if len(line) > args.max_length:
                check = False
                short_fn = fn[len(args.code_folder)+1:]
                print('[{}]\tline={}\t[{}>{}]'.format(short_fn, i+1, len(line), args.max_length))
    if not check:
        print('Codes are too long, please fix them.')
        sys.exit()
    
    content = []
    line_list = []
    for fn in file_list:
        if len(line_list) > 0:
            n = args.page_lines - len(line_list) % args.page_lines
            if n == args.page_lines:
                n = 0
            for i in range(n):
                line_list.append('\n')
        
        # add to content
        short_fn = fn[len(args.code_folder)+1:]
        content.append('({}) {}[{}]\n'.format(len(content) + 1, short_fn, int(len(line_list)/args.page_lines) + 1))

        # add title
        n = int((args.max_length - len(short_fn))/2)
        line_list.append('{}{}{}\n'.format('-'*n, short_fn, '-'*n))
        line_list.append('\n')

        with open(fn, 'r') as fr:
            line_list.extend(fr.readlines())
    if not os.path.exists(os.path.join('highlight/styles', args.style)):
        print('The style file [{}] is not exist.'.format(args.style))
        sys.exit()
    
    project_name = args.code_folder.split('/')[-1]

    head = """
        <!DOCTYPE html><html><head lang="en">
        <meta charset="UTF-8"><title>{}</title>
        <link rel="stylesheet" href="highlight/styles/{}">
        <script src="highlight/highlight.pack.js"></script>
        <body><script>hljs.initHighlightingOnLoad();</script>
        <pre><code class="python">""".format(project_name, args.style)
    tail = """</code></pre></body></html>"""

    with open(project_name + '.html', 'w') as fw:
        fw.write(head)
        fw.writelines(line_list)
        fw.write(tail)

    # save content
    with open(project_name + '_content.txt', 'w') as fw:
        fw.write(project_name + '\n')
        fw.writelines(content)


if __name__ == "__main__":
    main()


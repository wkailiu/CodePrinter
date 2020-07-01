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
      
    line_list = []
    for fn in file_list:
        if len(line_list) > 0:
            n = args.page_lines - len(line_list) % args.page_lines
            if n == args.page_lines:
                n = 0
            for i in range(n):
                line_list.append('\n')
        
        n = int((args.max_length - len(fn))/2)
        line_list.append('{}{}{}\n'.format('-'*n, fn, '-'*n))
        line_list.append('\n')
        i = 0
        with open(fn, 'r') as fr:
            line_list.extend(fr.readlines())
        
    head = """
        <!DOCTYPE html><html><head lang="en">
        <meta charset="UTF-8"><title>CodePrinter</title>
        <link rel="stylesheet" href="highlight/styles/default.css">
        <script src="highlight/highlight.pack.js"></script>
        <body><script>hljs.initHighlightingOnLoad();</script>
        <pre><code class="python">"""
    tail = """</code></pre></body></html>"""

    with open('CodePrinter.html', 'w') as fw:
        fw.write(head)
        fw.writelines(line_list)
        fw.write(tail)


if __name__ == "__main__":
    main()


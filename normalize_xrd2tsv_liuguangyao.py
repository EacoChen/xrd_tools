# -*- coding: UTF-8 -*-
import os
import argparse
from glob import glob


def parseArgs():
    parser = argparse.ArgumentParser(description='将xrd下机文件中的ras转化为txt文件，能够导入search-match中')

    parser.add_argument('-i', '--input', type = str, required=True, help = '包含ras文件的文件夹路径或者ras文件路径')
    parser.add_argument('-o', '--output', type = str, required=False, help = '输出文件夹，若不指定，默认为输入文件夹')
    parser.add_argument('-s', '--suffix', type = str, default='ras', required=False, help = '输入文件的后缀名，默认为ras')

    return parser.parse_args()


def std_file(infile,output):
    file_name = os.path.basename(infile).split('.')[0]
    if output == None:
        output = os.path.join(os.path.dirname(infile), f'{file_name}.tsv')
    else:
        output = os.path.join(os.path.abspath(output), f'{file_name}.tsv')

    text = open(infile, 'rb').read()
    text = text.decode('gbk')

    data = []
    flag = 0
    for line in text.split('\n'):
        if line.startswith('*RAS_INT_END'):
            flag = 0
        if flag == 1:
            data.append(line.replace(' ', '\t',1).replace(' 1.0000', ''))
        if line.startswith('*RAS_INT_START'):
            flag = 1

    with open(output, 'w') as f:
        f.write('\n'.join(data))


def main():
    arg = parseArgs()
    infile = arg.input
    suffix = arg.suffix
    output = arg.output

    if infile is None:
        raise Exception("You must specify the input file with -i, use --help to check the parameter.")
    infile = os.path.abspath(rf"{infile}")
    if os.path.isdir(infile):
        for file_name in glob(os.path.join(infile,f'*.{suffix}')):
            std_file(file_name,output)
    elif os.path.isfile(infile):
        std_file(infile,output)
    

if __name__ =='__main__':
    main()
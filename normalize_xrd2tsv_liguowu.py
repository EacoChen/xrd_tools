# -*- coding: UTF-8 -*-
import os
import argparse
from glob import glob


def parseArgs():
    parser = argparse.ArgumentParser(description='将xrd下机文件中的txt转化为tsv文件，能够导入search-match中')

    parser.add_argument('-i', '--input', type = str, required=True, help = '包含txt文件的文件夹路径或者txt文件路径')
    parser.add_argument('-o', '--output', type = str, required=False, help = '输出文件夹，若不指定，默认为输入文件夹')
    parser.add_argument('-s', '--suffix', type = str, default='txt', required=False, help = '输入文件的后缀名，默认为txt')
    parser.add_argument('-l', '--line', type = int, default=1, required=False, help='改变换行符，默认参数1，如果输出文件不能导入search-match就用2')

    return parser.parse_args()


def std_file(infile,output,line):
    file_name = os.path.basename(infile).split('.')[0]
    if output == None:
        output = os.path.join(os.path.dirname(infile), f'{file_name}.tsv')
    else:
        output = os.path.join(os.path.abspath(output), f'{file_name}.tsv')

    text = open(infile, 'rb').read()
    text = text.decode('gbk')

    data = []
    flag = 0
    if line == 1:
        sep = '\r\n'
    elif line == 2:
        sep = '\n'
    
    for line in text.split(sep):
        if flag == 1:
            data.append(line.replace(' ', '').replace(',', '\t', 1).replace(',', ''))
        if line.startswith('     Angle'):
            flag = 1

    with open(output, 'w') as f:
        f.write('\n'.join(data[:-1]))


def main():
    arg = parseArgs()
    infile = arg.input
    suffix = arg.suffix
    output = arg.output
    line = arg.line

    if infile is None:
        raise Exception("You must specify the input file with -i, use --help to check the parameter.")
    infile = os.path.abspath(rf"{infile}")
    if os.path.isdir(infile):
        for file_name in glob(os.path.join(infile,f'*.{suffix}')):
            std_file(file_name,output,line)
    elif os.path.isfile(infile):
        std_file(infile,output,line)
    

if __name__ =='__main__':
    main()
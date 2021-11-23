# -*- coding: UTF-8 -*-
import os
import click
from glob import glob


def std_file(infile,output):
    file_name = os.path.basename(infile).split('.')[0]
    if output == None:
        output = os.path.join(os.path.dirname(infile), f'{file_name}.tsv')
    else:
        output = os.path.join(os.path.abspath(output), f'{file_name}.tsv')

    text = open(infile, 'r').read()

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


@click.command()
@click.option("-i", "infile", required=True ,help="指定仪器输入的txt文件路径，可将脚本放在需要操作的文件下运行，"
                                   "或者使用绝对路径（使用绝对路径时，不能有数字开头的文件夹,文件"
                                   "名中有空格时应在参数中加引号如：\"work space\")")
@click.option("-o", "output", help="指定输出文件夹，默认为输入文件目录下.tsv文件")
@click.option("-s", "suffix", default='ras', help="指定输入文件后缀，默认ras")

def main(infile,output,suffix):
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
# -*- coding: UTF-8 -*-
import os
import click


@click.command()
@click.option("-i", "infile", help="指定仪器输出的txt文件路径，可将脚本放在需要操作的文件下运行，"
                                   "或者使用绝对路径（使用绝对路径时，不能有数字开头的文件夹,文件"
                                   "名中有空格时应在参数中加引号如：\"work space\")")
@click.option("-o", "output", help="指定输出文件名，默认为输入文件目录下.tsv文件")

def main(infile,output):
    if infile is None:
        raise Exception("You must specify the input file with -i, use --help to check the parameter.")
    infile = rf"{infile}"
    file_name = os.path.basename(infile).split('.')[0]
    if output == None:
        output = file_name + '.tsv'

    if '\\' in infile:
        DIRPATH = os.path.dirname(infile)
        filepath = infile
    else:
        DIRPATH = os.getcwd()
        filepath = os.path.join(DIRPATH, infile)
    text = open(filepath, 'r').read()

    data = []
    flag = 0
    for line in text.split('\n'):
        if flag == 1:
            data.append(line.replace(' ', '').replace(',', '\t', 1).replace(',', ''))
        if line.startswith('     Angle'):
            flag = 1

    with open(os.path.join(DIRPATH, output), 'w') as f:
        f.write('\n'.join(data))


if __name__ =='__main__':
    main()
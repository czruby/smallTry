import os
import sys


def main():
    indir = input("请输入dat文件路径")
    path = os.path.dirname(os.path.realpath(sys.argv[0]))
    outdir = path + '\output'

    if not os.path.exists(outdir):
        os.mkdir(outdir)
    # 获取文件夹下所有文件
    infiles = os.listdir(indir)

    # 计数成功的文件个数
    count = 0

    # 循环每个文件进行判断、转换
    for infile in infiles:
        # 获取文件名
        filename = infile[0:infile.find('.')]

        # 二进制读取文件
        f1 = open(os.path.join(indir, infile), 'rb')
        infilebytes = f1.read()
        newfile = []

        # 判断图片类型JPG，通过异或判定
        if (infilebytes[0] ^ 0xFF) == (infilebytes[1] ^ 0xD8):
            y1 = infilebytes[0] ^ 0xFF
            print('%s,文件是JPG图片，每个字节是根据0x%X异或进行加密' % (infile, y1))

            # 字节进行异或转换，组合成新的文件
            for i in infilebytes:
                newbyte = i ^ y1
                newfile.append(newbyte)
            newfile2 = bytes(newfile)

            # 写入新文件
            f2 = open(os.path.join(outdir, filename + '.jpg'), 'wb')
            f2.write(newfile2)
            count += 1

        # 判断图片类型PNG，通过异或判定
        elif (infilebytes[0] ^ 0x89) == (infilebytes[1] ^ 0x50):
            y1 = infilebytes[0] ^ 0x89
            print('%s,文件是PNG图片，每个字节是根据0x%X异或进行加密' % (infile, y1))
            for i in infilebytes:
                newbyte = i ^ y1
                newfile.append(newbyte)
            newfile2 = bytes(newfile)
            f2 = open(os.path.join(outdir, filename + '.png'), 'wb')
            f2.write(newfile2)
            count += 1

        # 判断图片类型GIF，通过异或判定
        elif (infilebytes[0] ^ 0x47) == (infilebytes[1] ^ 0x49):
            y1 = infilebytes[0] ^ 0x47
            print('%s,文件是GIF图片，每个字节是根据0x%X异或进行加密' % (infile, y1))
            for i in infilebytes:
                newbyte = i ^ y1
                newfile.append(newbyte)
            newfile2 = bytes(newfile)
            f2 = open(os.path.join(outdir, filename + '.gif'), 'wb')
            f2.write(newfile2)
            count += 1
        else:
            print('%s无法识别的类型！' % infile)
    print('识别出图片%d张' % count)


if __name__ == '__main__':
    main()
    input()

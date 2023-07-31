if __name__ == '__main__':
    qian = '<div class=\"wp-block-buttons\"><div class=\"wp-block-button\"><a class=\"wp-block-button__link\" href="'
    middle = "\" target=\"_blank\" rel=\"noreferrer noopener\">"
    last = "</a></div>"
    res = ''
    with open("1.txt", mode='r', encoding='utf-8') as f:
        my_str = f.read()
    my_str_list = my_str.split('\n')
    for i in my_str_list:
        res += qian
        res += i.split(' ')[1]
        res += middle
        res += i.split(' ')[0]
        res += last
    with open("1.txt", mode='w', encoding='utf-8') as f:
        f.write(res)

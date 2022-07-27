# Python 3.8.10
import os
import shutil

template = """
---
title: %s
---

"""
split_mark_all = "==========\n"
split_mark_inner = "\n"
split_mark_date = " "
books = {}
path = './kindle/'
dir_name = 'kindle'

def split_clippings():
    # 清空文件夹重建
    if os.path.exists(path):
        shutil.rmtree(dir_name)
    os.mkdir(dir_name)
    with open("My Clippings.txt", "r", encoding="utf-8") as f:
        content = f.read()
        
    arr = content.split(split_mark_all)

    for item in arr:
        # 每条笔记内部，数组存储分四部分 名称 位置 换行 笔记
        note = item.split(split_mark_inner)
        if len(note)<5:
            continue
        book_name = note[0]
        book_name = book_name[1:len(book_name)]
        if book_name in books:
            # 追加
            n = ''.join([note[3], '\n', note[1], '\n---\n\n'])
            books[book_name]['num'] = books[book_name]['num'] + 1
            books[book_name]['contents'].append(n)
        else:
            # 每本书第一条标注或笔记的日期
            date = note[1].split(split_mark_date)[7]
            y = date.index('年')
            m = date.index('月')
            d = date.index('日')
            # 去掉年月日加横杆
            date = '-'.join([date[0:y], date[y+1:m].zfill(2), date[m+1:d].zfill(2)])
            # 路径别带空格，不然index.md的markdown生成不了链接
            file_name = ''.join([path, date, '-', book_name.replace(' ', ''), '.md'])
            short_file_name = ''.join([date, '-', book_name.replace(' ', ''), '.html'])
            head = ''.join([template % book_name, note[3], '\n', note[1], '\n---\n\n'])

            # 写到字典
            books[book_name] = {
                'num':1,
                'file_name':file_name, 
                'short_file_name':short_file_name, 
                'first_date':date,
                'contents': [head]
            }

def generate_md_file():
    # 排序
    sorted_books = sorted(books, key = lambda i: books[i]['first_date'], reverse=True)
    index_file = path + 'index.md'
    with open(index_file, 'w') as f:
        f.write('## Kindle 读书笔记\n\n')
        for sorted_book_name in sorted_books:
            sorted_book = books[sorted_book_name]
            short_file_name = sorted_book['short_file_name']
            num = sorted_book['num']
            first_date = sorted_book['first_date']
            file_name = sorted_book['file_name']
            contents = sorted_book['contents']
            # 书籍信息
            f.write(''.join(['- [', sorted_book_name, '](/kindle/', short_file_name, ') / ', str(num), '条 / ', first_date, '\n']))
            # 根据书籍生成文件，写入笔记
            with open(file_name, 'a') as cf:
                for content in contents:
                    cf.write(content)

if __name__ == "__main__":
    print('============开始处理============')
    print('...')
    split_clippings()
    generate_md_file()
    print('============处理完毕============')

from ds.dataAnnotationHandler import DataAnnotationHandler
import settings


def print_things(things: set, msg: str):
    print()
    print(msg)
    count: int = 0
    for thing in things:
        count += 1
        print(thing, end=' ')
        if count == settings.PRINT_ITEM_NUM:
            count = 0
            print()


def main():
    # 执行检查
    checking = DataAnnotationHandler(settings.SOURCE_FILE, settings.MARKS, settings.TAGS)

    # 打印高频词文件
    if settings.OUTPUT_FREQUENT_FILE:
        with open('frequent.txt', 'w', encoding='utf-8') as file:
            for key, value in checking.words_sum.items():
                if value >= settings.FREQUENT_NUM and len(key) > 1:
                    file.write(key + "\n")

    # 打印朝代
    if settings.PRINT_DYNASTY:
        print_things(checking.dynasty, "dynasty:")

    # 打印作者
    if settings.PRINT_AUTHOR:
        print_things(checking.poets, "poets:")


if __name__ == '__main__':
    main()

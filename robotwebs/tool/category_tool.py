import threading

from robotwebs import MysqlTool


class Category:
    category_dict = None
    lock = threading.Lock()

    @staticmethod
    def init():
        categories = Category.get_category()
        Category.category_dict = Category.tuples_to_dict(categories)
        return Category.category_dict

    @staticmethod
    def update(category_name):
        Category.lock.acquire()  # 加锁，锁住相应的资源
        category_id = Category.save_category(category_name)
        Category.category_dict[category_name] = category_id
        Category.lock.release()  # 解锁，离开该资源
        return category_id

    @staticmethod
    def save_category(category_name):
        conn = MysqlTool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'insert into info_category(info_category_name) values(%s) ', category_name
        )
        id = int(cursor.lastrowid)
        conn.commit()
        conn.close()
        return id

    @staticmethod
    def get_category():
        conn = MysqlTool.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'select info_category_id, info_category_name from info_category'
        )
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def tuples_to_dict(tuples):
        dict = {}
        if len(tuples) != 0:
            for tuple in tuples:
                id = tuple[0]
                value = tuple[1]
                dict[value] = id
        return dict

dict = Category.init()
print(dict.get('a'))
print(dict)
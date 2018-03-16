from items import RobotOfWeekItem
from pipeline.mysql import Mysql
import logging


class RobotOfweekPipeline(object):

    '''
    The default pipeline invoke function
    '''
    def process_item(self, item, spider):
        conn = Mysql.get_connection()
        judge = item[RobotOfWeekItem.JUDGE]
        if judge == 1:
            self.insert_into_information(conn, item)
            self.insert_into_infocontent(conn, item)
            pass
        else:
            self.insert_into_infocontent(conn, item)
            pass
        conn.close()
        return item

    # 插入的表，此表需要事先建好
    def insert_into_information(self, conn, item):
        url = item[RobotOfWeekItem.LINK]
        title = item[RobotOfWeekItem.TITLE]
        summary = item[RobotOfWeekItem.SUMMARY]
        time = item[RobotOfWeekItem.RECORD_TIME]
        cursor = conn.cursor()
        cursor.execute(
            'insert into information(info_link, info_title, info_summary, info_release_time) values(%s,%s,%s,%s)',
            (url, title, summary, time)
        )
        conn.commit()

    def insert_into_infocontent(self, conn, item):
        cursor = conn.cursor()
        cursor.execute('select info_id from information where info_title = %s', item[RobotOfWeekItem.TITLE])
        result = (cursor.fetchone())
        if result is not None:
            info_id = int(result[0])
            content = item[RobotOfWeekItem.CONTENT]
            content = content[0]
            cursor.execute('insert into infocontent(info_id, info_main) values(%s, %s)', (info_id, content))
            conn.commit()
        else:
            print("查询不到该记录：" + item[RobotOfWeekItem.TITLE])
        pass

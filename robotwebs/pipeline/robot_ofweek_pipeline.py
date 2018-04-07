import re

from robotwebs.items import RobotOfWeekItem
from robotwebs.tool.mysql import MysqlTool


class RobotOfweekPipeline(object):

    '''
    The default pipeline invoke function
    '''
    def process_item(self, item, spider):
        if isinstance(item, RobotOfWeekItem):
            conn = MysqlTool.get_connection()
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
        release_time = item[RobotOfWeekItem.RELEASE_TIME]
        record_time = item[RobotOfWeekItem.RECORD_TIME]
        category_name = item[RobotOfWeekItem.CATEGORY_NAME]
        category_id = item[RobotOfWeekItem.CATEGORY_ID]
        source = item[RobotOfWeekItem.SOURCE]
        cursor = conn.cursor()
        cursor.execute(
            'insert into '
            'information(info_link, info_title, info_summary, '
            'info_release_time, info_record_time, info_category_id, info_source) '
            'values(%s,%s,%s,%s,%s,%s,%s)',
            (url, title, summary, release_time, record_time, category_id, source)
        )
        conn.commit()

    def insert_into_infocontent(self, conn, item):
        cursor = conn.cursor()
        cursor.execute('select info_id from information where info_title = %s', item[RobotOfWeekItem.TITLE])
        result = (cursor.fetchone())
        if result is not None:
            info_id = int(result[0])
            content = item[RobotOfWeekItem.CONTENT][0]
            page = item[RobotOfWeekItem.PAGE]
            cursor.execute('insert into info_content(info_id, info_main, current_page) values(%s, %s, %s)',
                           (info_id, content, page))
            conn.commit()
        else:
            print("查询不到该记录：" + item[RobotOfWeekItem.TITLE])
            result = re.match('http://robot.ofweek.com/\d+-\d+/ART-\d+-\d+-\d+.html$',
                              item[RobotOfWeekItem.LINK]).group()
            if result is not None:
                self.insert_into_information(conn, item)
                self.insert_into_infocontent(conn, item)
        pass

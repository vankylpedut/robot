from robotwebs.items import RobotItemManager
from robotwebs.pipeline.mysql import Mysql


class RobotOfweekPipeline(object):

    '''
    The default pipeline invoke function
    '''
    def process_item(self, item, spider):
        conn = Mysql.get_connection()
        judge = item[RobotItemManager.JUDGE]
        if judge == 0:
            self.insert_into_information(conn, item)
            self.insert_into_infocontent(conn, item)
        else:
            self.insert_into_infocontent(conn, item)
        conn.close()
        return item

    # 插入的表，此表需要事先建好
    def insert_into_information(self, conn, item):
        url = item[RobotItemManager.LINK]
        title = item[RobotItemManager.TITLE]
        summary = item[RobotItemManager.SUMMARY]
        time = item[RobotItemManager.RECORD_TIME]
        cursor = conn.cursor()
        cursor.execute(
            'insert into information(info_link, info_title, info_summary, info_release_time) values(%s,%s,%s,%s)',
            (url, title, summary, time)
        )
        conn.commit()

    def insert_into_infocontent(self, conn, item):
        cursor = conn.cursor()
        cursor.execute('select info_id from information where info_link = %s', item[RobotItemManager.LINK])
        result = (cursor.fetchone())
        info_id = int(result[0])
        content = item[RobotItemManager.CONTENT]
        content = content[0]
        cursor.execute('insert into infocontent(info_id, info_main) values(%s, %s)', (info_id, content))
        conn.commit()
        pass

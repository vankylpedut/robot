from datetime import datetime
import time


import robotwebs.settings
from robotwebs.tool.mysql import MysqlTool
from robotwebs.tool.category_tool import Category
from robotwebs.tool.variable_settings import VariableSettings

# 截止时间获取
if settings.DEADLINE_IS_TODAY is True:
    # DEADLINE设为今天策略
    datetime_format = '%Y-%m-%d %H:%M'
    str_time = time.strftime('%Y-%m-%d', time.localtime()) + ' 00:00'
else:
    # 从settings读取DEADLINE策略
    datetime_format = settings.DATETIME_FORMAT
    str_time = settings.DEADLINE_TIME
deadline_time = datetime.strptime(str_time, datetime_format)


if settings.IS_FORCE is True:
    # 根据DEADLINE获取文章
    deadline_time = deadline_time
    result = MysqlTool.get_limit_info_release_time(time=deadline_time)
    time_list = MysqlTool.tuple_tuple_to_list(result)
    time_list = MysqlTool.date_list_str_to_date(time_list, '%Y-%m-%d %H:%M:%S')
else:
    # 从之前记录获取截止日期
    result = MysqlTool.get_info_release_time(30)
    length = len(result)
    if length > 0:  # 数据库获取时间
        deadline_time = result[length - 1][0]
        if isinstance(deadline_time, str):
            deadline_time = datetime.strptime(deadline_time, datetime_format)
        time_list = MysqlTool.tuple_tuple_to_list(result)
        time_list = MysqlTool.date_list_str_to_date(time_list, '%Y-%m-%d %H:%M')
    else:
        # 数据库没有可获取时间,根据DEADLINE获取
        deadline_time = deadline_time
        time_list = []
VariableSettings.DEADLINE_TIME = deadline_time
VariableSettings.TIME_LIST = time_list
print(VariableSettings.DEADLINE_TIME)
print(VariableSettings.TIME_LIST)
pass

VariableSettings.CATEGORY_DICT = Category.init()

# 创建日志路径
# sep = os.path.sep  # 获取系统分割符
# wp = os.getcwd()
# lp = settings.LOG_FILE
# lp = lp[0:lp.rfind('/')].replace('/', sep)
# path = wp + sep + lp
# if os.path.exists(path) is not True:
#     os.makedirs(path)
# pass

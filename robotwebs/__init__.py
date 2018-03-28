from datetime import datetime

import os

import robotwebs.settings
from robotwebs.tool.mysql import MysqlTool
from robotwebs.tool.variable_settings import VariableSettings

# 截止时间获取
str_time = settings.DEADLINE_TIME
datetime_format = settings.DATETIME_FORMAT
deadline_time = datetime.strptime(str_time, datetime_format)
if settings.IS_FORCE is True:  # settings强制开关已打开，按配置文件时间为准
    VariableSettings.DEADLINE_TIME = deadline_time
    result = MysqlTool.get_limit_info_record_time(time=deadline_time)
    VariableSettings.TIME_LIST = MysqlTool.tuple_tuple_to_list(result)
else:
    result = MysqlTool.get_info_record_time(30)
    length = len(result)
    if length > 0:  # 数据库获取时间
        VariableSettings.DEADLINE_TIME = result[length - 1][0]
        VariableSettings.TIME_LIST = MysqlTool.tuple_tuple_to_list(result)
    else:  # 数据库没有可获取时间
        VariableSettings.DEADLINE_TIME = deadline_time
        VariableSettings.TIME_LIST = []
print(VariableSettings.DEADLINE_TIME)
print(VariableSettings.TIME_LIST)
pass

# 创建日志路径
sep = os.path.sep  # 获取系统分割符
wp = os.getcwd()
lp = settings.LOG_FILE
lp = lp[0:lp.rfind('/')].replace('/', sep)

path = wp + sep + lp
if os.path.exists(path) is not True:
    os.makedirs(path)
pass

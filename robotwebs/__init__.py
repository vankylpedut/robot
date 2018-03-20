from datetime import datetime

import settings
from tool.mysql import MysqlTool
from tool.variable_settings import VariableSettings

# 截止时间获取
str_time = settings.DEADLINE_TIME
datetime_format = settings.DATETIME_FORMAT
deadline_time = datetime.strptime(str_time, datetime_format)
if settings.IS_FORCE:   # settings强制开关已打开，按配置文件时间为准
    VariableSettings.DEADLINE_TIME = deadline_time
    result = MysqlTool.get_limit_info_record_time(time=deadline_time)
    VariableSettings.TIME_LIST = MysqlTool.tuple_tuple_to_list(result)
else:
    result = MysqlTool.get_info_record_time()
    if len(result) > 0:  # 数据库获取时间
        VariableSettings.DEADLINE_TIME = result[0][0]
        VariableSettings.TIME_LIST = MysqlTool.tuple_tuple_to_list(result)
    else:  # 数据库没有可获取时间
        VariableSettings.DEADLINE_TIME = deadline_time
        VariableSettings.TIME_LIST = []
print(VariableSettings.DEADLINE_TIME)
print(VariableSettings.TIME_LIST)
pass

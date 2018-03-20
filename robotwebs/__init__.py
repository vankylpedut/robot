import datetime
import re

from tool.mysql import MysqlTool
from tool.variable_settings import VariableSettings

MysqlTool.get_info_record_time()
print(VariableSettings.DEADLINE_TIME)
print(VariableSettings.TIME_LIST)
pass

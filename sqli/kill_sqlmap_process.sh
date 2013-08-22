kill `ps -ef | grep sqlmap | grep -v grep | awk '{print $2}'` > /dev/null 2>&1
exit 0
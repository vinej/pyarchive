from connection.connection import ConnectionMng
from ajson.archivejson import ArchiveJson
from connection.connection import ConnectionMng
from task.task import Task
import sys

def main() :
    args = sys.argv[1:]
    data = ArchiveJson().load(args[0])
    con = ConnectionMng(data)
    task = Task(data)
    task.run(con)
#def

main()
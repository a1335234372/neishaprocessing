# -*- coding:utf-8 -*-

from DB.DB import DB
import json
from util import Constants
import util.ErrorRecordUtil as eu
import importlib


def _checkMsg(jsonMsg):
    try:
        myJson = json.loads(jsonMsg.decode('utf-8'))
        if myJson["command"] and myJson["command"] in Constants.command:
            return myJson["command"]
        else:
            return False
    except Exception as ex:
        print(ex)
        return False


class ServiceFactory:

    def __init__(self):
        self.error = None
        self.record = eu.ErrorRecordUtil()
        try:
            DB.start()
        except Exception as e:
            print(e)
            self.error = "DB error"

    def excute(self,jsonMsg):
        if self.error:
            #return {"ret":500,"msg":self.error}
            self.record.recordSave(500,self.error,jsonMsg)

        command_name = _checkMsg(jsonMsg)
        if command_name:
            try:
                class_name = Constants.command[command_name]
                print(class_name)
                if class_name:
                    my_moudle = importlib.import_module("service." + class_name)
                    p = getattr(my_moudle,class_name)
                    command = p(jsonMsg)
                    result = command.excute()
                    if result['ret'] > 0:
                        self.record.recordSave(result['ret'], result['msg'], jsonMsg)
                    #return result
                else:
                    #return {"ret":500,"msg":"Not service class"}
                    self.record.recordSave(500, "Not service class", jsonMsg)
            except Exception as e:
                print(e)
                #return {"ret":500,"msg:":"class moudle error"}
                self.record.recordSave(500, "class moudle error", jsonMsg)
        #return {"ret":500,"msg":"command name error"}
        else:
            self.record.recordSave(500, "command name error", jsonMsg)

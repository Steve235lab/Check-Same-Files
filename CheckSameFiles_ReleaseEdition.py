# -*- coding: utf-8 -*-
"""
CheckSameFiles_ReleaseEdition.py

根据文件哈希值统计名称不同但内容完全相同的文件

这是基于"checkSameVideos.py"的发行版本软件的源代码，随附的应包含同名可执行程序

Created on Fri Dec  3 18:37:52 2021

@author: Steve D. J.

Copyright (c) 2021 Steve D. J.. All Rights Reserved.
"""


import os
import hashlib
import pandas as pd


def get_fNames(path):
    
    fName_list =os.listdir(path)
    return fName_list


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    md5 = myhash.hexdigest()
    return md5


# 程序入口
if __name__ == '__main__':
    
    print("CheckSameFiles_ReleaseEdition\nCopyright (c) 2021 Steve D. J.. All Rights Reserved.\n")
    
    folderPath = input("输入要检查的文件夹路径，或直接将文件夹拖入此命令行窗口：\n")
    folderPath = folderPath.replace('\'', '').replace('\"', '').replace('\\', '/')
    
    flag = 0
    while(flag == 0):
        try:
            nameList= get_fNames(folderPath)
            flag = 1
            
        except:
            folderPath = input("文件夹路径无效\n请重新输入：\n")
            folderPath = folderPath.replace('\'', '').replace('\"', '').replace('\\', '/')
    
    checkList = []
    hashList = []
    
    for i in nameList:
        flag = 0
        filePath = folderPath + "/" + i
        t_hash = GetFileMd5(filePath)
        
        for j in hashList:              # 与已经存在的hash值进行匹配
            if j == t_hash:             # 此hash已经存在：修改标志位
                flag = 1
                break
            
        if flag == 0:                   # 找到一个新的hash值
            hashList.append(t_hash)     # 存入hashList
            newLine = [t_hash, i]
            checkList.append(newLine)   # 作为一行新的数据存入checkList
            
        else:                           # hash值已存在，将文件名添加至对应行
            for k in range(0, len(checkList)):
                if t_hash == checkList[k][0]:
                    checkList[k].append(i)
                    
    # 将数据写入表格 
    excelPath = input("请将一个空白Excel表格文件拖入此命令行窗口：\n")    
    excelPath = excelPath.replace('\'', '').replace('\"', '').replace('\\', '/')
    
    flag = 0
    while(flag == 0):
        try:
            writer = pd.ExcelWriter(excelPath)
            
            a_checkList = pd.DataFrame(checkList)
            
            a_checkList.to_excel(writer, sheet_name='Sheet1', index = False)
            
            writer.save() 

            flag = 1
            
        except:
            excelPath = input("Excel文件路径无效\n请将一个空白Excel表格文件拖入此命令行窗口：\n")
            excelPath = excelPath.replace('\'', '').replace('\"', '').replace('\\', '/')
            
    print("\n已完成！\n请在" + excelPath + "中查看结果。\n")
               



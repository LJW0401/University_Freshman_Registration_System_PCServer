from flask import Flask, request, jsonify
import pandas as pd
import os
import sys

def description():
    '''
### 创建局域网网络服务\n
服务内容：\n
&emsp;一、通用服务，包括：\n
&emsp;&emsp;1. 检测服务连接情况\n
&emsp;二、与客户端进行数据交互，包括：\n
&emsp;&emsp;1. 上传收集到的材料的数据信息\n
&emsp;&emsp;2. 获取对象已经提交的数据信息\n
&emsp;三、与本机服务可视化界面进行数据交互，包括：\n
&emsp;&emsp;1. 获取所有对象材料收集情况的数据表格\n
&emsp;&emsp;2. 备份数据，保存为excel表格\n
    '''
    return
    
#所有数据均以字符串储存
app = Flask(__name__)
version = 'v1.0.0-beta'
needful_infomation = [] # 需要提交的材料信息列表
needful_infomation = ['户口本','毕业证','学位证']#,'照片','体检表','党团关系证明','学籍证明','学生证']
data_dict_initial = {
    '姓名':[],#默认列
    '身份证号':[],#默认列
    '学号':[],#默认列
    '户口本':[],
    '毕业证':[],
    '学位证':[]
}
data_frame = pd.DataFrame(data_dict_initial) # 数据表格
print(data_frame)

def AppPath():
    """获得主程序的路径"""
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__)            #没打包前的py目录



def Init():
    '''初始化'''
    return
    

def Backup():
    '''备份数据'''
    data_frame.to_excel(AppPath()+'/backup.xlsx', sheet_name='Sheet1', index=False)   
    return


# 这里是通用服务
@app.route('/connection_test', methods=['GET'])
def ConnectionTest():
    '''用于检测服务连接情况，如果连接上了则会返回connedted'''
    print('需要提交的材料信息：',needful_infomation)
    return "connected"


# 这里的函数是负责与客户端进行数据交互的
@app.route('/get_needful_upload_infomation', methods=['GET'])
def GetNeedfulUploadInfomation():
    '''用于获取需要提交的材料的信息，即具体有哪些材料需要提交'''
    global needful_infomation
    print('客户端请求获取需要提交的材料类型')
    data = {}
    for i,info_name in enumerate(needful_infomation):
        data[f'info{i}'] = info_name
    return jsonify(data)
    
    
@app.route('/upload_infomation', methods=['POST'])
def UploadInfomation():
    '''用于接收客户端上传的收集材料信息'''
    global data_frame
    json = request.json  # 获取 POST 请求中的 JSON 数据
    print(json)
    name = json['姓名']
    ID_number = json['身份证号']
    student_ID = json['学号']
    if ID_number != '':
        if ID_number in data_frame['身份证号'].tolist():
            row_index = data_frame[data_frame['身份证号']==ID_number].index.tolist()[0]# 获取该身份证对应的第一行该行的索引
            UpdateRow(row_index, json)
        else:
            AddNewRow(json)
    elif student_ID != '':
        if student_ID in data_frame['学号']:
            row_index = data_frame[data_frame['学号']==student_ID].index.tolist()[0]# 获取该学号对应的第一行该行的索引
            UpdateRow(row_index, json)
        else:
            AddNewRow(json)
    else:
        return 'Can_not_identify'
    
    Backup()
    print(data_frame)
    return "Received"


def UpdateSheet(row_index, json):
    '''弃用'''
    raise RuntimeError('该方法已弃用')
    global data_frame
    columns = data_frame.columns.tolist()
    for column in columns:
        if column in json:
            if json[column] != data_frame.loc[row_index, column]:
                data_frame.loc[row_index, column] = json[column]
    
    
def UpdateRow(row_index, json):
    '''更新行内容'''
    global data_frame
    columns = data_frame.columns.tolist()
    for column in columns:
        if column in json:
            if json[column] != data_frame.loc[row_index, column]:
                data_frame.loc[row_index, column] = json[column]


def AddNewRow(json):
    '''添加一行新数据'''
    global data_frame
    new_row = {}
    for data in json:
        new_row[data] = json[data]
    new_row_index = data_frame.shape[0]
    data_frame.loc[new_row_index] = new_row


@app.route('/get_infomation', methods=['GET', 'POST'])
def GetInfomation():
    '''TODO:测试可靠性'''
    '''通过对象信息获取该对象目前已经提交的信息'''
    global data_frame
    json = request.json  # 获取 POST 请求中的 JSON 数据
    print(json)
    name = json['姓名']
    ID_number = json['身份证号']
    student_ID = json['学号']
    if ID_number != '':
        if ID_number in data_frame['身份证号'].tolist():
            row_index = data_frame[data_frame['身份证号']==ID_number].index.tolist()[0]# 获取该身份证对应的第一行该行的索引
            return_json = data_frame.iloc[row_index].to_dict()
            return jsonify(return_json)
        else:
            return 'No_data'
    elif student_ID != '':
        if student_ID in data_frame['学号']:
            row_index = data_frame[data_frame['学号']==student_ID].index.tolist()[0]# 获取该学号对应的第一行该行的索引
            return_json = data_frame.iloc[row_index].to_dict()
            return jsonify(return_json)
        else:
            return 'No_data'
    else:
        return 'Can_not_identify'


# 与本机服务可视化界面进行数据交互
@app.route('/get_data_sheet', methods=['GET'])
def GetDataSheet():
    '''获取所有对象材料收集情况的数据表格'''
    global data_frame
    # 将DataFrame转换为字典
    dict_by_columns = data_frame.to_dict()
    json = {
        'columns':data_frame.columns.tolist(),#为了防止顺序错乱，这里将列名单独传输，后续依照这个顺序复原
        'dict_by_columns':dict_by_columns
    }
    return jsonify(json)


@app.route('/recover', methods=['GET'])
def Recover():
    '''恢复备份的数据信息'''
    global data_frame, needful_infomation
    data_frame_backup = pd.read_excel(AppPath()+'/backup.xlsx', dtype=str)
    print('')
    print('')
    print('')
    print(data_frame_backup)
    print('')
    print('')
    print('')
    data_frame = data_frame_backup
    columns = data_frame.columns.tolist()
    needful_infomation = columns[3:]
    json = {'needful_infomation':needful_infomation}
    return jsonify(json)


@app.route('/set', methods=['POST'])
def Set():
    '''设置需要提交的材料信息'''
    global needful_infomation,data_frame
    needful_infomation_tmp = request.json['needful_info']
    for nf in needful_infomation_tmp:
        if nf not in needful_infomation:
            new_column = ['0']*data_frame.shape[0]
            data_frame[nf] = new_column #在数据表格中增加一列
    for nf in needful_infomation:
        if nf not in needful_infomation_tmp:
            del data_frame[nf]#在数据表格中删除一列
    needful_infomation = needful_infomation_tmp.copy()
    print(data_frame)
    return "Server is setted."




if __name__ == '__main__':
    Init()
    print('\n\n\n')
    print('欢迎使用新生报到材料收集系统！')
    print(version)
    print('\n\n\n')
    app.run(host="0.0.0.0",port=5000)#,debug=True)

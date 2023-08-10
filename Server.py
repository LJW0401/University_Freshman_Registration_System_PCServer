from flask import Flask, request

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
    

app = Flask(__name__)



# 这里是通用服务
@app.route('/connection_test', methods=['GET'])
def ConnectionTest():
    '''用于检测服务连接情况，如果连接上了则会返回connedted'''
    return "connected"


# 这里的函数是负责与客户端进行数据交互的
@app.route('/get_needful_upload_infomation', methods=['GET'])
def GetNeedfulUploadInfomation():
    '''用于获取需要提交的材料的信息，即具体有哪些材料需要提交'''
    return "is developing..."
    
    
@app.route('/upload_infomation', methods=['POST'])
def UploadInfomation():
    '''用于接收客户端上传的收集材料信息'''
    data = request.json  # 获取 POST 请求中的 JSON 数据
    print(data)
    return f"This is a POST request with JSON data: {data}"


# 获取已提交的信息
@app.route('/get_infomation', methods=['GET', 'POST'])
def GetInfomation():
    '''通过对象信息获取该对象目前已经提交的信息'''
    return "This is a GET request."


# 与本机服务可视化界面进行数据交互
@app.route('/get_data_sheet', methods=['GET'])
def GetDataSheet():
    '''获取所有对象材料收集情况的数据表格'''
    return "This is a GET request."

@app.route('/back_up', methods=['GET'])
def back_up():
    '''备份数据信息'''
    return "Data have been backed up."

def init():
    '''初始化'''
    return
    
    
if __name__ == '__main__':
    init()
    print('\n\n\n欢迎使用新生报到材料收集系统！\n\n\n')
    app.run(host="0.0.0.0",port=5000)#,debug=True)

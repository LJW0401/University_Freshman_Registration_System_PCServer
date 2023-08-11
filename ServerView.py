import socket
import tkinter as tk
import tkinter.ttk
import tkinter.messagebox
import requests
import pandas as pd

def GetLocalIP():
    # 获取本机主机名
    host_name = socket.gethostname()
    # 获取主机名对应的IP地址
    ip_address = socket.gethostbyname(host_name)
    return ip_address

# local_ip = GetLocalIP()
# print("本机IP地址:", local_ip)

MAX_TIMEOUT = 1 # 最大超时时间(s)
MAX_INFOMATION = 15 # 最大信息个数

CONNECTED = 0
DISCONNECTED = 1

class Server_View():
    def __init__(self) -> None:
        self.host_ip = GetLocalIP()
        self.port = '5000'
        self.version = 'v1.0.0-alpha'

        self.window = tk.Tk()
        self.window.title(f'新生报到材料辅助收集系统服务端 {self.version}')
        self.window.geometry('700x600')
        self.window.resizable(0, 0)
        
        self.needful_infomation = [ # 需要提交的材料信息列表
            '户口本','毕业证','学位证','照片','体检表','党团关系证明','学籍证明','学生证'
            ]
        self.connect_state = DISCONNECTED # 连接状态
        
        
        self.CreateWidgets()
    
    
    def CreateWidgets(self):
        self.Frame_ConnectionTest = tk.LabelFrame(
            self.window,
            text="服务状态监测",
            font=('微软雅黑',10),
            bd=2,
            relief="groove",
            )
        self.Frame_ConnectionTest.place(x=10, y=5, width=210, height=110)
        self.CreateWidgets_Frame_ConnectionTest()
        
        self.Frame_Settings = tk.LabelFrame(
            self.window,
            text="设置相关信息",
            font=('微软雅黑',10),
            bd=2,
            relief="groove",
            )
        self.Frame_Settings.place(x=230, y=5, width=460, height=110)
        self.CreateWidgets_Frame_Settings()
        
        self.Frame_OperationBar = tk.LabelFrame(
            self.window,
            text="操作栏",
            font=('微软雅黑',10),
            bd=2,
            relief="groove",
            )
        self.Frame_OperationBar.place(x=10, y=120, width=120, height=450)
        self.CreateWidgets_Frame_OperationBar()
        
        self.Frame_DataTable = tk.LabelFrame(
            self.window,
            text="提交状态数据表格",
            font=('微软雅黑',10),
            bd=2,
            relief="groove",
            )
        self.Frame_DataTable.place(x=140, y=120, width=550, height=450)
    
    
    def CreateWidgets_Frame_OperationBar(self):
        button_width = 105
        button_height = 30
        self.Button_UpdateDataTable = tk.Button(#用于更新数据表格的按钮
            self.Frame_OperationBar,
            text='更新数据表格',
            font=('微软雅黑',10),
            command=self.BlankFunction,
            )
        self.Button_UpdateDataTable.place(x=5, y=0, width=button_width, height=button_height)
        
        self.Button_Recover = tk.Button(#用于备份恢复的按钮
            self.Frame_OperationBar,
            text='恢复备份数据',
            font=('微软雅黑',10),
            command=self.BlankFunction,
            )
        self.Button_Recover.place(x=5, y=int(button_height*1.2), width=button_width, height=button_height)
        
        
    def CreateWidgets_Frame_Settings(self):
        self.LabelPrompt_NeedfulInfomation = tk.Label(#用于显示提示需要提交的材料类型
            self.Frame_Settings,
            text='需要提交的材料类型：',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.LabelPrompt_NeedfulInfomation.place(x=5, y=0, width=130, height=20)

        self.Combobox_NeedfulInfomation = tkinter.ttk.Combobox(#用于创建、增删需要提交的信息
                        self.Frame_Settings,
                        width=10,height=1,
                        font=('微软雅黑', 10),
                        values=self.needful_infomation,
                        state='normal'
                    )
        self.Combobox_NeedfulInfomation.place(x=140, y=0, width=120, height=20)
        if self.needful_infomation.__len__()>0:
            self.Combobox_NeedfulInfomation.set(self.needful_infomation[0])
        self.Combobox_NeedfulInfomation.bind("<Return>", self.Combobox_NeedfulInfomation_OnReturn)#按回车键增加内容
        self.Combobox_NeedfulInfomation.bind("<Escape>", self.Combobox_NeedfulInfomation_OnEscape)#按esc键删除内容
        
        self.Button_UploadToServer = tk.Button(#用于将需要提交的信息等设置上传到服务中
            self.Frame_Settings,
            text='上传至服务器',
            font=('微软雅黑',10),
            command=self.Button_UploadToServer_Click,
            )
        self.Button_UploadToServer.place(x=270, y=-5, width=90, height=30)

        self.LabelPrompt_NameList = tk.Label(#用于显示提示电子名单的路径
            self.Frame_Settings,
            text='电子名单路径：',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.LabelPrompt_NameList.place(x=5, y=30, width=130, height=20)

        self.Entry_NameList = tk.Entry(#用于输入电子名单的路径
            self.Frame_Settings,
            font=('微软雅黑',10),
            state='readonly',
            )
        self.Entry_NameList.place(x=100, y=30, width=350, height=20)

        self.LabelPrompt_NameList = tk.Label(#用于显示提示电子照片文件夹的路径
            self.Frame_Settings,
            text='电子照片文件夹路径：',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.LabelPrompt_NameList.place(x=5, y=60, width=130, height=20)
        
        self.Entry_NameList = tk.Entry(#用于输入电子照片文件夹的路径
            self.Frame_Settings,
            font=('微软雅黑',10),
            state='readonly',
            )
        self.Entry_NameList.place(x=140, y=60, width=310, height=20)
    
    
    def Combobox_NeedfulInfomation_OnEscape(self,event):#用于删除发送数据
        '''当按下Esc键的时候删除需要提交的信息'''
        index = self.Combobox_NeedfulInfomation.current()
        if index == -1:#如果在数据列表中找不到则不进行任何操作直接返回
            pass
            # return
        
        self.needful_infomation.pop(index)
        self.Combobox_NeedfulInfomation.configure(values=self.needful_infomation)
        
        if self.needful_infomation.__len__() == 0:#如果没数据了就设为空
            self.Combobox_NeedfulInfomation.set('')
        elif index == self.needful_infomation.__len__():#如果删除的是最后一个数据则跳转到最后一个数据
            self.Combobox_NeedfulInfomation.set(self.needful_infomation[self.needful_infomation.__len__()-1])#删除后跳转到第一个数据
        else:
            self.Combobox_NeedfulInfomation.set(self.needful_infomation[index])
        # print(self.Combobox_NeedfulInfomation.current())
        # print(index)
        # print(self.needful_infomation)
    
        
    def Combobox_NeedfulInfomation_OnReturn(self,event):#用于输入内容及检测是否添加数据
        '''当按下回车键的时候添加需要提交的信息到列表中'''
        if self.Combobox_NeedfulInfomation.get() == '':
            tkinter.messagebox.showwarning(title='提示', message='需要提交的信息不能为空！')
        else:
            if self.Combobox_NeedfulInfomation.current()==-1 and self.needful_infomation.__len__()<MAX_INFOMATION:#发送数据名称不存在则添加新的发送数据
                info_name = self.Combobox_NeedfulInfomation.get()
                self.needful_infomation.append(info_name)
                
                self.Combobox_NeedfulInfomation.configure(values=self.needful_infomation)
            
        
        
    def CreateWidgets_Frame_ConnectionTest(self):
        self.Label_ConnectionTestSignal = tk.Label(#用于显示是否连接到服务器的信号灯
            self.Frame_ConnectionTest,
            background="red",
            )
        self.Label_ConnectionTestSignal.place(x=5, y=0, width=20, height=20)
        
        self.Label_ConnectionTest = tk.Label(#显示是否连接到服务器的文字
            self.Frame_ConnectionTest,
            text='服务未开启',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.Label_ConnectionTest.place(x=30, y=0, width=70, height=20)
        
        self.Button_ConnectToServer = tk.Button(#用于连接到服务器的按钮
            self.Frame_ConnectionTest,
            text='检测状态',
            font=('微软雅黑',10),
            command=self.Button_ConnectToServer_Click,
            )
        self.Button_ConnectToServer.place(x=103, y=-3, width=90, height=26)
        
        self.Label_HostIP = tk.Label(#显示服务器（本机）IP地址
            self.Frame_ConnectionTest,
            text=f'服务器IP：{self.host_ip}',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.Label_HostIP.place(x=5, y=30, width=180, height=20)
        
        self.Label_Port = tk.Label(#显示服务器（本机）服务开放的端口
            self.Frame_ConnectionTest,
            text=f'服务使用端口：{self.port}',
            font=('微软雅黑',10),
            anchor='w',
            )
        self.Label_Port.place(x=5, y=55, width=180, height=20)
        
    
    def Button_UploadToServer_Click(self):
        '''TODO:完成将相关设置传递到服务器的功能'''
        if self.connect_state == DISCONNECTED:
            tkinter.messagebox.showwarning(title='提示', message='服务未开启！')
            return
        elif self.connect_state == CONNECTED:
            json_data = {'needful_info':self.needful_infomation}
            response = requests.post(
                f'http://127.0.0.1:5000/set',
                json=json_data,
                timeout=MAX_TIMEOUT
                )
            print(response.text)
    
    
    def Button_ConnectToServer_Click(self):
        self.host_ip = GetLocalIP()
        self.Label_HostIP['text'] = f'服务器IP：{self.host_ip}'
        try:
            response = requests.get(
                f'http://127.0.0.1:5000/connection_test',
                timeout=MAX_TIMEOUT,
                )
            if response.status_code==200:
                if response.text=='connected':
                    self.connect_state = CONNECTED
            else:
                self.connect_state = DISCONNECTED
            self.SetConnectState()
            if self.connect_state == CONNECTED:
                self.window.after(5000, self.Button_ConnectToServer_Click)#每隔xs自动检测一次连接状态
        except:
            self.connect_state = DISCONNECTED
            self.SetConnectState()
        
        
    def SetConnectState(self):
        if self.connect_state == CONNECTED:
            self.Label_ConnectionTestSignal['background'] = 'green'
            self.Label_ConnectionTest['text'] = '服务已开启'
        elif self.connect_state == DISCONNECTED:
            self.Label_ConnectionTestSignal['background'] = 'red'
            self.Label_ConnectionTest['text'] = '服务未开启'
    
    
    def AutoConnectionTest(self):
        '''DEPRECATED(小企鹅)'''
        '''自动检测与服务器的连接状态'''
        raise RuntimeError('该方法已弃用')
        if self.connect_state == DISCONNECTED:
            return
        self.Button_ConnectToServer_Click()
        self.window.after(1000, self.AutoConnectionTest)
        
    
    def BlankFunction(self):
        tkinter.messagebox.showwarning(title='提示', message='正在使用空函数')
        
        
    def Run(self):
        self.window.mainloop()

if __name__ == '__main__':
    server_view = Server_View()
    server_view.Run()
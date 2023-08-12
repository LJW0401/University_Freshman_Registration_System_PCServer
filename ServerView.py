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


MAX_TIMEOUT = 1 # 最大超时时间(s)
MAX_INFOMATION = 15 # 最大信息个数

CONNECTED = 0
DISCONNECTED = 1

class Server_View():
    def __init__(self) -> None:
        self.host_ip = GetLocalIP()
        self.port = '5000'
        self.version = 'v1.0.0-beta'

        self.window = tk.Tk()
        self.window.title(f'新生报到材料辅助收集系统服务端 {self.version}')
        self.window.geometry('700x600')
        self.window.resizable(0, 0)
        
        self.needful_infomation = [ # 需要提交的材料信息列表
            '户口本','毕业证','学位证','照片','体检表','党团关系证明','学籍证明','学生证'
            ]
        self.data_frame = pd.DataFrame() # 用于存储数据的DataFrame        
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
        self.CreateWidgets_Frame_DataTable()
    
    def CreateWidgets_Frame_DataTable(self):
        self.TreeView_DataFrame = tkinter.ttk.Treeview(
            self.Frame_DataTable, 
            columns=["1", "2", "3"],
            show='headings'
            )
        self.TreeView_DataFrame.place(x=5, y=5, width=510, height=410)
        
        # 创建Scrollbar组件
        self.Scrollbar_DataFrame = tk.Scrollbar(self.Frame_DataTable)
        self.Scrollbar_DataFrame.place(x=515, y=5, width=20, height=410)
        # 绑定Scrollbar和Treeview
        self.Scrollbar_DataFrame.config(command=self.TreeView_DataFrame.yview)
        self.TreeView_DataFrame.configure(yscrollcommand=self.Scrollbar_DataFrame.set)
        
        
        self.AddTestDataToTreeView()
        # self.UpdateTreeView()
        
    def AddTestDataToTreeView(self):
        # 设置列标题
        self.TreeView_DataFrame.heading("1", text="姓名")
        self.TreeView_DataFrame.heading("2", text="身份证号")
        self.TreeView_DataFrame.heading("3", text="学号")
        # 设置列的宽度
        self.TreeView_DataFrame.column("1", width=50, anchor='center')
        self.TreeView_DataFrame.column("2", width=50, anchor='center')
        self.TreeView_DataFrame.column("3", width=50, anchor='center')

        # 插入行数据
        for i in range(10):
            self.TreeView_DataFrame.insert("", "end", values=("123", "123", "666"))
            self.TreeView_DataFrame.insert("", "end", values=("222", "333", "444"))
            self.TreeView_DataFrame.insert("", "end", values=("454", "154", "143"))
            self.TreeView_DataFrame.insert("", "end", values=["114", "312", "214"])
        self.TreeView_DataFrame.insert("", "end", values=("114"))
        self.TreeView_DataFrame.insert("", 2, values=("数据1", "数据2", "数据3"))

        # self.SwapColumns(1,3)#第一列为1
        # self.TreeView_DataFrame.delete(*self.TreeView_DataFrame.get_children())
        
    
    def SwapColumns(self, column1:int, column2:int):
        '''交换TreeView两列的数据'''
        items = self.TreeView_DataFrame.get_children()
        for item in items:
            values = list(self.TreeView_DataFrame.item(item, "values"))  # 将元组转换为列表
            values[column1-1], values[column2-1] = values[column2-1], values[column1-1]
            self.TreeView_DataFrame.item(item, values=tuple(values))  # 将列表转换回元组
            
        # 获取列1的标题和宽度
        heading1 = self.TreeView_DataFrame.heading(column1, "text")
        width1 = self.TreeView_DataFrame.column(column1, "width")

        # 获取列2的标题和宽度
        heading2 = self.TreeView_DataFrame.heading(column2, "text")
        width2 = self.TreeView_DataFrame.column(column2, "width")

        # 设置列1的标题和宽度为列2的值
        self.TreeView_DataFrame.heading(column1, text=heading2)
        self.TreeView_DataFrame.column(column1, width=width2)

        # 设置列2的标题和宽度为列1的值
        self.TreeView_DataFrame.heading(column2, text=heading1)
        self.TreeView_DataFrame.column(column2, width=width1)
    
    
    def AddNewColumn(self, column_name:str):
        pass
    
    
    def ChangeColumnName(self, column_name:str):
        pass
    
    
    def DeleteColumn(self, column_name:str):
        pass
    
        
    def CreateWidgets_Frame_OperationBar(self):
        button_width = 105
        button_height = 30
        self.Button_UpdateDataTable = tk.Button(#用于更新数据表格的按钮
            self.Frame_OperationBar,
            text='更新数据表格',
            font=('微软雅黑',10),
            command=self.Button_UpdateDataTable_Click,
            )
        self.Button_UpdateDataTable.place(x=5, y=0, width=button_width, height=button_height)
        
        self.Button_Recover = tk.Button(#用于备份恢复的按钮
            self.Frame_OperationBar,
            text='恢复备份数据',
            font=('微软雅黑',10),
            command=self.Button_Recover_Click,
            )
        self.Button_Recover.place(x=5, y=int(button_height*1.2), width=button_width, height=button_height)


    def UpdateTreeView(self):
        #直接无脑更新控件算了
        column_names = self.data_frame.columns.tolist()
        self.TreeView_DataFrame = tkinter.ttk.Treeview(
            self.Frame_DataTable, 
            columns=column_names,
            show='headings'
            )
        self.TreeView_DataFrame.place(x=5, y=5, width=450, height=350)
        # 绑定Scrollbar和Treeview
        self.Scrollbar_DataFrame.config(command=self.TreeView_DataFrame.yview)
        self.TreeView_DataFrame.configure(yscrollcommand=self.Scrollbar_DataFrame.set)
        for i,column_name in enumerate(column_names,0):
            #更新列名
            self.TreeView_DataFrame.heading(i, text=column_name)
            self.TreeView_DataFrame.column(i, width=50, anchor='center')
        for i in range(self.data_frame.shape[0]):
            #添加行信息
            row = self.data_frame.iloc[i].to_list()
            self.TreeView_DataFrame.insert("", "end", values=row)
        # #第1步，清除原有数据
        # self.TreeView_DataFrame.delete(*self.TreeView_DataFrame.get_children())
        # #第2部，检查列名是否匹配
        # data_frame_column_names = self.data_frame.columns.tolist()
        # TreeView_column_names = []
        # for column_id in self.TreeView_DataFrame["columns"]:#获取TreeView的所有列名
        #     column_name = self.TreeView_DataFrame.heading(column_id, "text")
        #     TreeView_column_names.append(column_name)
        # print('\n\n')
        # print(TreeView_column_names)
        # print(data_frame_column_names)
        # if TreeView_column_names == data_frame_column_names:
        #     for i in range(self.data_frame.shape[0]):
        #         row = self.data_frame.iloc[i].to_list()
        #         self.TreeView_DataFrame.insert("", "end", values=row)#将数据添加到TreeView中
        # else:
        #     # 先不搞什么优化了，直接无脑清零，重新标列，然后添加数据内容
        #     # 直接无脑赋值算了
        #     # for i,column_name in enumerate(data_frame_column_names,1):
        #     for i in range(max(TreeView_column_names.__len__(),data_frame_column_names.__len__())):
        #         if i < data_frame_column_names.__len__():
        #             column_name = data_frame_column_names[i]
        #             self.TreeView_DataFrame.column(i, width=50, anchor='center')
        #             self.TreeView_DataFrame.heading(i, text=column_name)
        #         else:
        #             #删除多余的列
        #     # if TreeView_column_names.__len__() > data_frame_column_names.__len__():#如果TreeView的列数比DataFrame的列数多就删除多余的
        #     #     #TODO:删除多余的列
        #     #     pass
        #     # # elif TreeView_column_names.__len__() < data_frame_column_names.__len__():#如果TreeView的列数比DataFrame的列数少就添加少的
        #     # else:
        #     #     #TODO:添加缺少的列
        #     #     for i,column_name in enumerate(data_frame_column_names,1):
        #     #         # if i <= TreeView_column_names.__len__():#给已有的列更换列名
        #     #         #     self.TreeView_DataFrame.heading(i, text=column_name)
        #     #         # else:#添加新的列
        #     #         #     self.TreeView_DataFrame.column(i, width=50, anchor='center')
        #     #         #     self.TreeView_DataFrame.heading(i, text=column_name)
                    
        #     #         #或许可以直接无脑赋值
        #     #         self.TreeView_DataFrame.column(i, width=50, anchor='center')
        #     #         self.TreeView_DataFrame.heading(i, text=column_name)
                    
        #     # # else:#相同时直接更换列名（）考虑合并到上面
        #     # #     pass
    
    
    def Button_UpdateDataTable_Click(self):
        '''TODO:更新Server返回的json数据，以符合json'''
        if self.connect_state == DISCONNECTED:
            tkinter.messagebox.showwarning(title='提示', message='服务未开启！')
            return
        elif self.connect_state == CONNECTED:
            #方案1：直接通过网络与服务器在本地传输表格
            #方案2：从本地的备份文件中加载表格
            #目前使用的是方案1
            # try:
            if 1:
                response = requests.get(
                    f'http://127.0.0.1:5000/get_data_sheet',
                    timeout=MAX_TIMEOUT
                    )
                print(response.status_code)
                print(type(response.status_code))
                if response.status_code == 200:
                    json = response.json()
                    #将数据按照原来的列顺序恢复成pandas数据表
                    columns = json['columns']
                    dict_by_columns_json = json['dict_by_columns']
                    dict_by_columns = {}
                    for column in columns:
                        dict_by_columns[column] = dict_by_columns_json[column]
                    self.data_frame = pd.DataFrame(dict_by_columns)
                    print(columns)
                    print(self.data_frame)
                    
                    #将数据表格显示到TreeView中
                    self.UpdateTreeView()
                    tkinter.messagebox.showinfo(title='提示', message='数据更新成功！')
                else:
                    tkinter.messagebox.showerror(title='错误', message='数据更新失败！')
            # except:
            #     tkinter.messagebox.showerror(title='错误', message='数据更新失败！')


    def Button_Recover_Click(self):
        if self.connect_state == DISCONNECTED:
            tkinter.messagebox.showwarning(title='提示', message='服务未开启！')
            return
        elif self.connect_state == CONNECTED:
            try:
                response = requests.get(
                    f'http://127.0.0.1:5000/recover'
                    )
                if response.status_code == 200:
                    json = response.json()
                    self.needful_infomation = json['needful_infomation']
                    self.Combobox_NeedfulInfomation.configure(values=self.needful_infomation)
                    if self.needful_infomation.__len__()>0:
                        self.Combobox_NeedfulInfomation.set(self.needful_infomation[0])
                    else:
                        self.Combobox_NeedfulInfomation.set('')
                        
                    print(json['needful_infomation'])
                    tkinter.messagebox.showinfo(title='提示', message='备份恢复成功！')
                else:
                    tkinter.messagebox.showerror(title='错误', message='备份恢复失败！')
            except:
                tkinter.messagebox.showerror(title='错误', message='备份恢复失败！')
                
    
    
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
        self.Combobox_NeedfulInfomation.configure(height=5)#设置下拉列表显示5个选项
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
                #后面别忘了改回5000
                self.window.after(60000, self.Button_ConnectToServer_Click)#每隔xs自动检测一次连接状态
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
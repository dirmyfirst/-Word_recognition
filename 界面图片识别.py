import wx
import wx.xrc
from aip import AipOcr
import time

class MyFrame1(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=wx.EmptyString, pos=wx.DefaultPosition,
                          size=wx.Size(435, 417), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText2 = wx.StaticText(self, wx.ID_ANY, "通用票据识别：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer5.Add(self.m_staticText2, 2, wx.ALL, 5)

        self.m_filePicker2 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file", "*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_filePicker2.GetPickerCtrl().SetLabel("选择发票图片")
        bSizer5.Add(self.m_filePicker2, 8, wx.ALL, 5)

        bSizer2.Add(bSizer5, 2, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl1 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE)
        bSizer4.Add(self.m_textCtrl1, 8, wx.ALL | wx.SHAPED, 5)

        bSizer2.Add(bSizer4, 8, wx.EXPAND, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

        self.m_staticText1 = wx.StaticText(self, wx.ID_ANY, "图片文字识别：", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText1.Wrap(-1)
        bSizer6.Add(self.m_staticText1, 2, wx.ALL, 5)

        self.m_filePicker1 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, "Select a file", "*.*",
                                               wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE)
        self.m_filePicker1.GetPickerCtrl().SetLabel("选择文字图片")
        bSizer6.Add(self.m_filePicker1, 8, wx.ALL, 5)

        bSizer3.Add(bSizer6, 2, wx.EXPAND, 5)

        bSizer7 = wx.BoxSizer(wx.VERTICAL)

        self.m_textCtrl2 = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TE_MULTILINE)
        bSizer7.Add(self.m_textCtrl2, 8, wx.ALL | wx.SHAPED, 5)

        bSizer3.Add(bSizer7, 8, wx.EXPAND, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_filePicker2.Bind(wx.EVT_FILEPICKER_CHANGED, self.getfapiao)
        self.m_filePicker1.Bind(wx.EVT_FILEPICKER_CHANGED, self.getimage)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def getfapiao(self, event):
        self.get_file_name2 = self.m_filePicker2.GetTextCtrl().GetValue()
        self.get_getfapiao()
        event.Skip()

    def getimage(self, event):
        self.get_file_name1 = self.m_filePicker1.GetTextCtrl().GetValue()
        self.get_getimage()
        event.Skip()

    def get_file_content(self,filepath):
        with open(filepath, 'rb') as fp:
            return fp.read()

    def get_getimage(self):
        APP_ID = '14637674'
        API_KEY = 'D27ZHGnry02WQZlC35ThsoFc'
        SECRET_KEY = 'IQQhWeKqNscG6Wy5Xq3kVUkhGMiPP44D'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        image = self.get_file_content(self.get_file_name1)
        res = client.basicAccurate(image)
        for words in res['words_result']:
            for key, word in words.items():
                self.m_textCtrl2.AppendText(word + '\n')
                time_ = time.strftime("%Y-%m-%d-%H-%M-%S")
                time_file = time_ + '.txt'
                with open(time_file, 'a') as f:
                    f.write(word + '\n')

    def get_getfapiao(self):
        APP_ID = '14637674'
        API_KEY = 'D27ZHGnry02WQZlC35ThsoFc'
        SECRET_KEY = 'IQQhWeKqNscG6Wy5Xq3kVUkhGMiPP44D'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

        image = self.get_file_content(self.get_file_name2)
        res = client.receipt(image)
        print(res)
        for words in res['words_result']:
            for key,word in words.items():
                if key == 'words':
                    print(word)
                    self.m_textCtrl1.AppendText(word + '\n')


app = wx.App(False)
frame = MyFrame1(None)
frame.Show(True)
app.MainLoop()

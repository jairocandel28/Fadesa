#Inicia

import wx

class TestFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, wx.ID_ANY, title, pos=(0, 0), size=(320, 240))
        panel = wx.Panel(self, wx.ID_ANY)
        text = wx.StaticText(panel, wx.ID_ANY, "Hello, World!", wx.Point(10, 5), wx.Size(-1, -1))

class TestApp(wx.App):
    def OnInit(self):
        frame = TestFrame(None, wx.ID_ANY, "Hello, world!")
        self.SetTopWindow(frame)
        frame.Show(True)
        return True

if __name__ == '__main__':
    app = TestApp()
    app.MainLoop()
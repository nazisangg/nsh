import wx
from Player import Player
from Strategy import Strategy
# buzhidaoxu buxuyao maybe add one get_palyerstategy will be good in palyer


class nshUI(object):

    def __init__(self):
        app = wx.App() 
        window = wx.Frame(None, title = "Welcome", size = (400,300)) 
        panel = wx.Panel(window) 
        label = wx.StaticText(panel, label = "Hello World", pos = (100,100)) 
        window.Show(True) 
        app.MainLoop()


nshUI()

    


# -*- coding: utf-8 -*-
'''
Created on 2016/8/10

@author: RP_S
'''
import re

import wx

#import pyhk


#hot_key = pyhk.pyhk()

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, ID, title, pos, size, style)
        panel = wx.Panel(self, -1)
        
        #self.hot_key_id = self.reg_hot_key()
        
        self.init_icon()
        
        self.CenterOnScreen()
        
        self.rgb_re = re.compile(r'\d{1,3},\d{1,3},\d{1,3}')
        self.rgb_re_num = re.compile(r'\d+')
        self.hex_re = re.compile(r'#[a-fA-F0-9]{6}')
        
        t12 = wx.TextCtrl(panel, 12)
        t12.SetPosition((10, 10))
        t12.SetSize((100, 20))
        t12.Bind(wx.EVT_KEY_UP, self.refresh_color)
        self.t12 = t12
        
        t22 = wx.TextCtrl(panel, 22)
        t22.SetPosition((10, 40))
        t22.SetSize((100, 20))
        t22.Bind(wx.EVT_KEY_UP, self.refresh_color)
        self.t22 = t22
        
        t31 = wx.StaticText(panel, 31, '颜色:'.decode('utf-8'))
        t31.SetPosition((10, 70))
        t31.SetSize((50, 20))
        
        t32 = wx.StaticText(panel, 32)
        t32.SetPosition((50, 70))
        t32.SetSize((50, 20))
        self.color = t32
        
        self.Bind(wx.EVT_CLOSE, self.on_close)
    
    def on_close(self, evt):
        self.Destroy()
        self.tbicon.Destroy()
        #hot_key.removeHotkey(self.hot_key_id)
    
    def init_icon(self):
        my_icon = wx.EmptyIcon()
        my_icon.LoadFile('color_find.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(my_icon)
        self.tbicon = wx.TaskBarIcon()
        self.tbicon.SetIcon(my_icon, '颜色值转换器'.decode('utf-8'))
    
    #def reg_hot_key(self):
    #   return hot_key.addHotkey(['Ctrl', 'Alt', 'C'], self.on_hot_key)
    
    def on_hot_key(self):
        if self.IsShown():
            self.Iconize()
            self.Show(False)
        elif self.IsIconized():
            self.Iconize(False)
            self.Show(True)
            self.Raise()
            self.t12.SetFocus()
        
    def find_num(self, s):
        result = self.rgb_re_num.findall(s)
        if len(result) != 0:
            return result[0]
        return 0
    
    def to_hex_str(self, num):
        hex_num = hex(num)
        hex_str = str(hex_num)
        hex_str_num_part = hex_str[2:].upper()
        if len(hex_str_num_part) < 2:
            return '0' + hex_str_num_part
        return hex_str_num_part
        
    def parse_hex(self, s):
        r = s[1:3]
        g = s[3:5]
        b = s[5:7]
        dec_r = int(r, 16)
        dec_g = int(g, 16)
        dec_b = int(b, 16)
        return '%s,%s,%s' % (str(dec_r), str(dec_g), str(dec_b))
        
    def refresh_color(self, evt):
        source = evt.EventObject
        # id can be 12 or 22
        source_id = evt.Id
        if isinstance(source, wx.TextCtrl):
            val = source.GetValue()
           
            if re.match(self.rgb_re, val):
                nums = val.split(',')
                
                rgb_r = int(self.find_num(nums[0]))
                rgb_g = int(self.find_num(nums[1]))
                rgb_b = int(self.find_num(nums[2]))
                
                hex_color_str = "".join(('#', self.to_hex_str(rgb_r) , self.to_hex_str(rgb_g) , self.to_hex_str(rgb_b)))
                
                self.color.SetBackgroundColour(hex_color_str)
                
                if source_id == 12:
                    self.t22.SetValue(hex_color_str)
                else:
                    self.t12.SetValue(hex_color_str)
                    
            if re.match(self.hex_re, val):
                self.color.SetBackgroundColour(val)
                
                rgb_str = self.parse_hex(val)
                
                if source_id == 12:
                    self.t22.SetValue(rgb_str)
                else:
                    self.t12.SetValue(rgb_str)
            self.color.Refresh()
            
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None, -1, "ColorCoder", size=(100, 150), style=wx.DEFAULT_DIALOG_STYLE)
    frame.Show(True)
    app.MainLoop()
    

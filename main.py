import wx
import os,logging



class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(350, 350))
        panel = wx.Panel(self)
        logging.basicConfig(filename='example.log',level=logging.DEBUG)
        # ////////////////////////////////////////
        label = wx.StaticText(panel, label=" port number :", pos=(5, 20))
        self.txtPort = wx.TextCtrl(panel, pos=(100, 12),value="80", size=(200, 35))
        # ///////////////////////////////////////////
        label2 = wx.StaticText(panel, label=" host name :", pos=(5, 60))
        self.txtHotName = wx.TextCtrl(panel,value="site.com", pos=(100, 55), size=(200, 35))
        # /////////////////////////////////////////////
        label3 = wx.StaticText(
            panel, label=" Project path :", pos=(5, 110))
        self.txtProjectPath = wx.TextCtrl(panel, pos=(100, 100), size=(200, 35))
        # /////////////////////////////////////////////
        btn = wx.Button(panel, label='Generate', pos=(100, 155))
        btn.Bind(wx.EVT_BUTTON, self.Generate_Click)

        self.Show()

    def Generate_Click(self, event):
        dlg = wx.DirDialog(self, "Choose input directory", "",
                           wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK:
            self.txtProjectPath.Clear()
            self.txtProjectPath.SetValue(dlg.GetPath())
            # print('You selected: %s\n' % dlg.GetPath())
            self.addToHost(self)
            self.CreatVHost(self)
            os.system('sudo a2ensite '+self.txtHotName.GetValue()+'.conf')
            os.system('sudo service apache2 start')
            os.system('sudo service apache2 reload')

        dlg.Destroy()

    @staticmethod
    def addToHost(self):
        with open('/etc/hosts', 'rt') as f:
            s = f.read() + '\n' + '127.0.0.1\t\t'+self.txtHotName.GetValue()
            with open('/tmp/etc_hosts.tmp', 'wt') as outf:
                outf.write(s)
        cmd = 'mv /tmp/etc_hosts.tmp /etc/hosts'
        os.system(cmd)
    @staticmethod    
    def CreatVHost(self):
        # logging.info(strn)
        f=open('/etc/apache2/sites-available/'+self.txtHotName.GetValue()+'.conf',"w")
        text=' <VirtualHost '+self.txtHotName.GetValue()+':'+self.txtPort.GetValue()+'>\n'
        text+=' ServerAdmin admin@'+self.txtHotName.GetValue()+'\n'
        text+=' DocumentRoot '+self.txtProjectPath.GetValue()+'\n'
        text+='<Directory '+self.txtProjectPath.GetValue()+'>'+'\n'
        text+='AllowOverride All'+'\n'
        text+= 'Options None'+'\n'
        text+='Require all granted'+'\n'
        text+='</Directory>'+'\n'
        text+='ServerName '+self.txtHotName.GetValue()+'\n'
        text+=' ServerAlias www.'+self.txtHotName.GetValue()+'\n'
        text+=' ErrorLog ${APACHE_LOG_DIR}/error.log\nCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>'
        f.write(text)
        f.close()

app = wx.App()
Mywin(None, 'Moravel')
app.MainLoop()

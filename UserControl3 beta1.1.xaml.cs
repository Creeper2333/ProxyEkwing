using Fiddler;
using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace ProxyEk
{
    /// <summary>
    /// UserControl3.xaml 的交互逻辑
    /// </summary>
    public partial class UserControl3 : UserControl
    {
        private object oSecureEndpoint;
        private int iSecureEndpointPort;
        private string sSecureEndpointHostname;

        public UserControl3()
        {
        }

        public UserControl3(bool bty,bool invip,bool score,bool display)
        {
            string reppplace;
            Fiddler.FiddlerApplication.BeforeRequest += delegate (Fiddler.Session oS)
            {
                
                oS.bBufferResponse = false;
                

                if (oS.url.Contains("ekwing.com/exam/student/examload?id="))
                {
                    oS.bBufferResponse = true;
                    
                }
            };
            Fiddler.FiddlerApplication.BeforeResponse += delegate (Fiddler.Session oSession)
            {
                if (oSession.isHTTPS)
                {

                    if(invip == true)
                    {
                        oSession.utilDecodeResponse();

                        reppplace = oSession.GetResponseBodyAsString().Replace("/resource/exam/css/ek-base.css", "http://openedu.vaiwan.com/ek2-c.css");
                        oSession.utilSetResponseBody(reppplace);

                        reppplace = oSession.GetResponseBodyAsString().Replace("解锁VIP专属试题", "");
                        oSession.utilSetResponseBody(reppplace);//不重复写会失败

                        reppplace = oSession.GetResponseBodyAsString().Replace("收起所有VIP专属试题", "");
                        oSession.utilSetResponseBody(reppplace);

                        reppplace = oSession.GetResponseBodyAsString().Replace("iconfont", "");
                        if (oSession.GetResponseBodyAsString().Contains("/resource/exam/css/ek-base.css"))
                        {
                            //MessageBox.Show("1");
                        }
                        oSession.utilSetResponseBody(reppplace);
                    }

                }
            };
            try
            {
                Fiddler.FiddlerApplication.Startup(8080, true, true);
            }catch(Exception)
            {
                MessageBox.Show("出现了不可预知的错误，请重启软件");
                Environment.Exit(0);
            }
            oSecureEndpoint = FiddlerApplication.CreateProxyEndpoint(iSecureEndpointPort, true, sSecureEndpointHostname);
            InitializeComponent();
            System.Diagnostics.Process.Start("http://ekwing.com");

        }
    }
}

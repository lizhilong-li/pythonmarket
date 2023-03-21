Market-Data-Get
主要用于商超数据获取;

目前已经支持烟台振华

后续持续增加;

1首先安装python 3.11; 安装方式自行百度;

2安装2个支持库  BeautifulSoup4 requests  (win+r  然后输入cmd)

    pip install requests

    pip install BeatifulSoup4

3 代码补充

    rev_data = {
        'loginname': '振华登录名',
        'pwd': '密码',
        'sale_begin_date': '2022-01-01',  # 开始日期sale_end_date
        'sale_end_date': '2022-01-01',  # 结束日期
        'type': 4
    }
将上面代码中loginname pwd sale_begin_date sale_end_date 分别换成 用户名和密码以及 采集的开始日期和结束日期;

4 执行程序 (win+r  然后输入cmd)
    
    python3 YanTaiZhenHua.py

如果需要帮助请联系QQ:99365865 备注:商超采集
 
    





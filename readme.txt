

http://saoleibao.a.baimeidashu.com/

----------------------------------------
docker compose 启动：


构建和启动服务：

# 方法1：使用 docker-compose
docker-compose up --build -d


# 方法2：使用启动脚本
chmod +x start.sh
./start.sh

docker-compose logs -f


停止服务：
# 方法1：使用 docker-compose
docker-compose down

# 方法2：使用停止脚本
chmod +x stop.sh
./stop.sh

--------------------------

http://saoleibao.a.baimeidashu.com/



2025年9月14日 新建仓库


pip install flask requests beautifulsoup4 lxml


4. 使用方法
安装依赖：
pip install -r requirements.txt
运行应用：
python app.py

访问系统： 打开浏览器访问 http://localhost:5000


5 获取5000多只股票列表， getstocklist

-----------------------------需求------------------


模拟真实的浏览器去查询

接口如下：http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/bxb.html?code=xxxxxx&color=0


通过浏览器，把xxxxxx换成想要查询的股票代码即可，例如

http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/bxb.html?code=000001&color=0


原样返回原始界面信息


直接在新窗口中打开原始URL

查询的时候可以输入股票名字，然后后台自动转化为股票代码进行查询

生成单独股票代码映射表保存在stockcode.txt 文件中


按照stockcode.txt 文本格式，列出 A股所有股票的对应代码


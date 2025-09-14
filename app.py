from flask import Flask, render_template, request, jsonify
import requests
import re
import os

app = Flask(__name__)

# 创建一个Session对象来保持会话，模拟真实浏览器
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache'
})

def load_stock_codes():
    """
    从stockcode.txt文件加载股票代码映射表
    """
    stock_dict = {}
    try:
        # 获取stockcode.txt文件的路径
        stockcode_file = os.path.join(os.path.dirname(__file__), 'stockcode.txt')
        print(f"尝试加载股票代码文件: {stockcode_file}")

        # 读取文件内容
        with open(stockcode_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '=' in line:
                    name, code = line.split('=', 1)
                    stock_dict[name] = code
        print(f"成功加载 {len(stock_dict)} 个股票代码")
    except FileNotFoundError:
        print("警告: 未找到stockcode.txt文件")
    except Exception as e:
        print(f"读取stockcode.txt文件时出错: {e}")

    return stock_dict

# 加载股票代码映射表
print("开始加载股票代码映射表...")
STOCK_NAME_TO_CODE = load_stock_codes()
print("股票代码映射表加载完成")

@app.route('/')
def index():
    """
    主页面，提供股票代码输入表单
    """
    print("访问主页")
    return render_template('index.html')

@app.route('/query_stock', methods=['POST'])
def query_stock():
    """
    查询股票信息的接口
    支持股票代码和股票名称查询
    """
    print("收到查询请求")
    stock_input = request.form.get('stock_input')
    print(f'用户输入: {stock_input}')

    if not stock_input:
        print("未输入股票代码或名称")
        return jsonify({'error': '请输入股票代码或名称'}), 400

    # 判断输入是股票代码还是名称
    stock_code = stock_input
    if re.match(r'^[\u4e00-\u9fa5]+$', stock_input):  # 如果是中文（股票名称）
        print(f"识别为股票名称: {stock_input}")
        stock_code = STOCK_NAME_TO_CODE.get(stock_input)
        print(f'股票名称"{stock_input}"对应的代码是: {stock_code}')
        if not stock_code:
            print(f"未找到股票名称对应的代码: {stock_input}")
            return jsonify({'error': f'未找到股票"{stock_input}"对应的代码'}), 400
    elif not re.match(r'^\d{6}$', stock_input):  # 如果不是6位数字代码
        print("输入格式不正确")
        return jsonify({'error': '请输入正确的6位股票代码或股票名称'}), 400
    else:
        print(f"识别为股票代码: {stock_input}")

    try:
        # 构造请求URL
        url = f"http://page3.tdx.com.cn:7615/site/pcwebcall_static/bxb/bxb.html?code={stock_code}&color=0"
        print(f"构造请求URL: {url}")

        # 使用Session发送请求，模拟真实浏览器行为
        response = session.get(url, timeout=10)
        response.raise_for_status()

        # 设置正确的编码
        response.encoding = 'utf-8'

        # 返回查询结果页面URL，让前端在新窗口打开
        print("请求成功，返回URL")
        return jsonify({'url': url})

    except requests.exceptions.Timeout:
        print("请求超时")
        return jsonify({'error': '请求超时，请稍后再试'}), 500
    except requests.exceptions.ConnectionError:
        print("连接错误")
        return jsonify({'error': '连接错误，无法访问目标服务器'}), 500
    except requests.RequestException as e:
        print(f"请求异常: {e}")
        return jsonify({'error': f'请求失败: {str(e)}'}), 500

if __name__ == '__main__':
    print("启动Flask应用...")
    app.run(debug=True, host='0.0.0.0', port=5010)

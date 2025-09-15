import tushare as ts
import pandas as pd
import os
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

def get_all_a_stocks_with_tushare():
    """
    使用tushare获取A股所有股票代码
    """
    print("正在使用tushare获取A股股票数据...")

    try:


        # 从环境变量中获取tushare token
        token = os.getenv('TUSHARE_TOKEN')
        if not token:
            print("未找到TUSHARE_TOKEN环境变量，请在.env文件中设置")
            return []
        print(f"Token长度: {len(token)}")  # 调试信息
        print(token)
        # 设置tushare token
        ts.set_token(token)

        pro = ts.pro_api()


        # 获取股票列表
        # 获取沪深A股基本信息
        stocks_df = pro.stock_basic(exchange='', list_status='L',
                                    fields='ts_code,symbol,name,area,industry,list_date')

        if stocks_df is not None and not stocks_df.empty:
            print(f"成功获取到 {len(stocks_df)} 只股票数据")

            # 转换为stockcode.txt格式
            stock_list = []
            for index, row in stocks_df.iterrows():
                code = str(row['symbol']).strip()
                name = str(row['name']).strip().replace(' ', '').replace('*', '')

                # 确保代码是6位数字格式
                if len(code) == 6 and code.isdigit():
                    stock_list.append(f"{name}={code}")

            # 去重并排序
            stock_list = sorted(list(set(stock_list)))
            return stock_list
        else:
            print("未能获取到股票数据")
            return []

    except Exception as e:
        print(f"使用tushare获取股票数据时出错: {e}")
        print("可能需要先注册tushare账号并获取token")
        return []


def get_stocks_without_token():
    """
    不使用token的替代方法（获取部分数据）
    """
    print("尝试不使用token获取股票数据...")

    try:
        # 获取部分股票数据（不需要token）
        # 这个方法可能获取的数据有限
        stocks_df = ts.get_stock_basics()

        if stocks_df is not None and not stocks_df.empty:
            print(f"成功获取到 {len(stocks_df)} 只股票数据")

            # 转换为stockcode.txt格式
            stock_list = []
            for code, row in stocks_df.iterrows():
                name = str(row['name']).strip().replace(' ', '').replace('*', '')

                # 确保代码是6位数字格式
                if len(code) == 6 and code.isdigit():
                    stock_list.append(f"{name}={code}")

            # 去重并排序
            stock_list = sorted(list(set(stock_list)))
            return stock_list
        else:
            print("未能获取到股票数据")
            return []

    except Exception as e:
        print(f"不使用token获取股票数据时出错: {e}")
        return []


def save_stocks_to_file(stocks, filename='stockcode.txt'):
    """
    保存股票代码到文件
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            for stock in stocks:
                f.write(f"{stock}\n")
        print(f"成功保存 {len(stocks)} 只股票到 {filename}")
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False


def main():
    """
    主函数
    """
    print("开始获取A股所有股票代码...")

    # 首先尝试使用tushare获取股票数据
    stocks = get_all_a_stocks_with_tushare()

    # 如果失败，尝试不使用token的方法
    if not stocks:
        stocks = get_stocks_without_token()

    if stocks:
        if save_stocks_to_file(stocks):
            print("股票代码文件生成成功！")
            print("文件已保存为: stockcode.txt")
        else:
            print("股票代码文件生成失败！")
    else:
        print("未能获取到股票数据，生成示例文件...")
        # 生成示例文件
        example_stocks = [
            "平安银行=000001",
            "万科A=000002",
            "中国平安=000003",
            "中国国贸=000004",
            "世纪星源=000005",
            "深振业A=000006",
            "全新好=000007",
            "神州高铁=000008",
            "中国宝安=000009",
            "ST天龙=000010"
        ]
        save_stocks_to_file(example_stocks, 'stockcode_example.txt')
        print("已生成示例文件 stockcode_example.txt")


if __name__ == "__main__":
    main()

# python-web-crawler--Instagram-

运行脚本时，会请求输入两个参数（id和after）
这两个参数都可以在对应的Ins页面上，鼠标右键>检查元素>Network(网络)>XHR，找到左侧的？query_hash=02e....这个数据，并且点击它，会看到右侧有对应的Headers栏，然后下拉到最下面，就可看到有一个叫做“查询字符串参数”的数值，复制对应的id和after参数到脚本即可

举例:
id：7683921212
after：QVFDSkVna3UyZjh4MjRiOHB6OEZWek5GZERmejhJMVFBSHhuTTFJY2x6b0VZQnpWc2dVTDZCT05wUGlKLWQ3SWZsN1JrSVB4RXQ4eWNIdlRZY09pUXlYXw

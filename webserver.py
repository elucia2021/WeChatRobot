from flask import Flask, request
import logging
from datetime import datetime, timedelta
import os

basedir = os.path.abspath(".")
logfile = os.path.join(basedir, "logs", "webserver.log") #放入logs日志里
logging.basicConfig(level=logging.DEBUG, handlers=[logging.FileHandler(filename=logfile, encoding='utf-8')])

class Webserver:
    def __init__(self, robot=None, host='127.0.0.1', port=8000, debug=False, name=__name__) -> None:
        self.host = host
        self. port = port
        self.app = Flask(name)
        self._register_routes()
        self.robot = robot
        self.debug = debug
        self.logger = logging.getLogger(__name__)

    def _register_routes(self):
        """注册路由到 Flask 应用"""
        # 示例路由：根路径
        @self.app.route('/')
        def home():
            return "Welcome to the FlaskService!"

        # 示例路由：API接口
        @self.app.route('/api/senddata', methods=['POST'])
        def send_data():
            data = request.form.to_dict()  #接收form-data格式
            try:
                if 'atlist' in data:
                    self.robot.sendTextMsg(data['msg'], data['roomid'], data['atlist'])
                else:
                    self.robot.sendTextMsg(data['msg'], data['roomid'])
                self.logger.info('发送消息' + data['msg'])
                return "发送成功"

            except Exception as e:
                self.logger.info('发送消息失败')
                return "信息发送失败，失败内容: /\n " + e
    def configure(self, config_dict):
        """动态更新配置"""
        self.app.config.update(config_dict)

    def run(self):
        """启动 Flask 服务"""
        self.app.run(host=self.host, port=self.port, debug=self.debug, threaded=True)
        self.logger.info('flask服务已启动')


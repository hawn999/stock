#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import datetime as dt
from dateutil import tz
from instock.trade.robot.infrastructure.default_handler import DefaultLogHandler
from instock.trade.robot.infrastructure.strategy_template import StrategyTemplate




class Strategy(StrategyTemplate):
    name = 'stratey1'

    def init(self):
        # 通过下面的方式来获取时间戳
        # now_dt = self.clock_engine.now_dt
        # now = self.clock_engine.now
        # now = time.time()

        # 注册时钟事件
        clock_type = self.name
        moment = dt.time(14, 54, 30, tzinfo=tz.tzlocal())
        self.clock_engine.register_moment(clock_type, moment)

        # 注册时钟间隔事件, 不在交易阶段也会触发, clock_type == minute_interval
        minute_interval = 1.5
        self.clock_engine.register_interval(minute_interval, trading=False)

    def strategy(self):
        buy_stock = [('000001', 1, 100)]
        sell_stock = [('000001', 100, 100)]
        # --------写交易策略---------

        # --------写交易策略---------
        for buy in buy_stock:
            self.user.buy(buy[0], price=buy[1], amount=buy[3])
        for sell in sell_stock:
            self.user.sell(sell[0], price=sell[1], amount=sell[3])

        self.log.info('检查持仓')
        self.log.info(self.user.balance)
        self.log.info('\n')

    def clock(self, event):
        """在交易时间会定时推送 clock 事件
        :param event: event.data.clock_event 为 [0.5, 1, 3, 5, 15, 30, 60] 单位为分钟,  ['open', 'close'] 为开市、收市
            event.data.trading_state  bool 是否处于交易时间
        """
        if event.data.clock_event == self.name:
            self.strategy()
        elif event.data.clock_event == 1.5:
            pass

    def log_handler(self):
        """自定义 log 记录方式"""
        cpath_current = os.path.dirname(os.path.dirname(__file__))
        cpath = os.path.abspath(os.path.join(cpath_current, os.pardir))
        log_filepath = os.path.join(cpath, 'log', f'{self.name}.log')
        return DefaultLogHandler(self.name, log_type='file', filepath=log_filepath)

    def shutdown(self):
        """
        关闭进程前的调用
        :return:
        """
        self.log.info("假装在关闭前保存了策略数据")

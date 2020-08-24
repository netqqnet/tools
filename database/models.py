#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time,uuid
from datetime import datetime
from lib.orm import Model, StringField, BooleanField, FloatField, TextField,IntegerField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


# 定义PowerData对象:
class PowerData(Model):
    # 表的名字:
    __table__ = 'power_data'
    # 表的结构:
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    switch_id = StringField(ddl='varchar(20)')
    curve_id = StringField(ddl='varchar(20)')
    pos_sign = IntegerField()
    lable = IntegerField()
    start_time = FloatField(default=datetime.now())
    length = IntegerField()
    period = IntegerField()
    power_data = TextField()
    all_data = TextField()

# 定义TrainingData对象:
class TrainingData(Model):
    # 表的名字:
    __table__ = 'training_data'
    # 表的结构:
    training_no = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    status = IntegerField() 
    accuracy_data = StringField(ddl='varchar(20)')
    loss_data = StringField(ddl='varchar(20)')
    start_time = FloatField(default=datetime.now())
    end_time = FloatField(default=datetime.now())

# 定义TmpTrainingData对象:
class TmpTrainingData(Model):
    # 表的名字:
    __table__ = 'tmp_training_data'
    # 表的结构:
    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    training_no = StringField(ddl='varchar(50)')
    step = IntegerField()
    accuracy_rate = StringField(ddl='varchar(20)')
    loss_val = StringField(ddl='varchar(20)')
    create_time = FloatField(default=datetime.now())
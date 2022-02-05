from django.db import models

# Create your models here.
#客户表  主键身份证号
class customer(models.Model):
    name = models.CharField('姓名',max_length=10,default='')
    sex = models.CharField('性别',max_length=10,default='')
    age = models.IntegerField('年龄',default='')
    Idcard = models.CharField('身份证号',max_length=18,default='')
    mobile = models.CharField('联系方式',max_length=11,default='')
    province = models.CharField('省',max_length=8,default='内蒙古自治区')
    city = models.CharField('市',max_length=8,default='乌兰察布市')
    address = models.CharField('详细地址',max_length=30,default='')
    addTime = models.DateField('创建日期',auto_now_add=True)
    note = models.CharField('备注(不超过30个字)',max_length=30,default='')
    class Meta:
        db_table = 'customer'
# 供货商表 主键供货公司
class supplier(models.Model):
    name = models.CharField('供货公司',max_length=25,default='')
    address = models.CharField('供货商地址',max_length=35,default='')
    mobile = models.CharField('联系方式', max_length=11, default='')
    type = models.CharField('供货类型',max_length=50,default='')
    note = models.CharField('备注(不超过30个字)',max_length=30,default='')
    class Meta:
        db_table = 'supplier'
#经销商表
class agent(models.Model):
    name = models.CharField('经销公司',max_length=25,default='')
    address = models.CharField('经销商地址',max_length=35,default='')
    mobile = models.CharField('联系方式',max_length=11,default='')
    type = models.CharField('需货类型',max_length=50,default='')
    note = models.CharField('备注(不超过30个字)',max_length=30,default='')
    class Meta:
        db_table = 'agent'
# 库存管理 主键自动生成
class inventory(models.Model):
    model = models.CharField('型号',max_length=15,default='')
    storage = models.IntegerField('库存量',default='0')
    note = models.CharField('备注(不超过30个字)',max_length=30,default='')
    class Meta:
        db_table = 'inventory'
# #供货信息表 主键自动生成
class supply(models.Model):
    ordernumber = models.CharField('供货单号',max_length=50)
    supplier = models.CharField('供货商',max_length=25)
    supply_time = models.CharField('供货时间',max_length=15)
    type = models.CharField('供货类型',max_length=10)
    number = models.IntegerField('供货数量',default=0)
    price = models.DecimalField('供货单价',max_digits=8,decimal_places=2)
    totalprice = models.DecimalField('供货总价',max_digits=10,decimal_places=2)
    note = models.CharField('备注',max_length=50)
    class Meta:
        db_table = 'supply'
#型号表
class Type(models.Model):
    type = models.CharField('型号',max_length=20)
    note = models.CharField('备注',max_length=50)
    class Meta:
        db_table='type'
#销售管理表
class Sell(models.Model):
    name = models.CharField('交易人',max_length=15)
    model = models.CharField('型号', max_length=20)
    tradingamount = models.IntegerField('数量',default='0')
    price = models.DecimalField('交易金额',max_digits=10,decimal_places=2,default='0')
    payamount = models.IntegerField('支付金额',default='0')
    paymethods = models.CharField('支付方式',max_length=10,default='0')
    arrearamount = models.DecimalField('拖欠金额',max_digits=10,decimal_places=2,default='0')
    date = models.CharField('供货时间',max_length=15)
    note = models.CharField('备注', max_length=50,default='')
    class Meta:
        db_table='sell'
#产品信息表
class Productinfo(models.Model):
    model = models.CharField('产品',max_length=10)
    information = models.TextField('产品介绍',blank=True,null=True)
    picture = models.ImageField('图片',upload_to='picture_show',default='')#图片信息
    create_date = models.DateField('创建日期',auto_now_add=True)
    alter_date = models.DateField('修改日期',auto_now=True)
    release = models.CharField('是否已发布', max_length=5, default='否')
    class Meta:
        db_table = 'productshow'

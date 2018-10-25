from django.db import models


# Create your models here.
class Users(models.Model):
    # sex/性别属性选项
    gender = (
        ('male', '男'),
        ('female', '女'),
    )

    # 创建表的字段
    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(max_length=50, unique=True)
    sex = models.CharField(max_length=12, choices=gender, default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    # 重载字符串，用于人性化显示信息
    def __str__(self):
        return self.name

    # 表的信息重载
    class Meta:
        ordering = ['-c_time']
        verbose_name = '用户'
        verbose_name_plural = '用户'





import re
from datetime import datetime
from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from MxShop.settings import REGEX_MOBILE
from .models import VerifyCode

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param mobile:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已存在")

        # 验证手机号码是否合法
        if re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count() > 0:
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile


class UserRegSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=4, min_length=4, help_text="验证码",
                                 error_messages={
                                     "blank": "请输入验证码",
                                     "required": "请输入验证码",
                                     "max_length": "验证码格式错误",
                                     "min_length": "验证码格式错误"
                                 })
    username = serializers.CharField(required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=User.objects.all(), message="用户已存在")])

    # 填写错误，长度错误，过期
    def validate_code(self, code):
        # 不用get，异常2种：1. 可以会有2个相同的验证码，会有2条数据，不用get 2.取不到数据时
        # try:
        #     veryfy_records = VerifyCode.objects.get(mobile=self.initial_data["username"])
        # except VerifyCode.DoesNotExist as e :
        #     pass
        # except VerifyCode.MultipleObjectsReturned as e :
        #     pass

        # 前端传过来的值放在 initial_data里
        veryfy_records = VerifyCode.objects.filter(mobile=self.initial_data["username"]).order_by("-add_time")
        if veryfy_records:
            last_record = veryfy_records[0]

            five_minutes_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if five_minutes_ago < last_record.add_time:
                raise serializers.ValidationError("验证码过期")

            if last_record != code:
                raise serializers.ValidationError("验证码错误")
        else:
            raise serializers.ValidationError("验证码错误")

    def validate(self, attrs):
        attrs["mobile"] = attrs["username"]
        del attrs["code"]
        return attrs

    class Meta:
        model = User
        fields = ("username", "code", "mobile")
        # code 在userprofile里是没有的，是我们自己添加的

#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from logging import getLogger
from service_authlib.core.server.common.models.user import OAuth2UserModel
from service_authlib.core.server.common.grants.password import PasswordGrant as BasePasswordGrant

logger = getLogger(__name__)


class PasswordGrant(BasePasswordGrant):
    """ 密码模式 """

    def authenticate_user(self, username: t.Text, password: t.Text) -> t.Union[OAuth2UserModel, None]:
        """ 用户模型对象用户

        @param username: 账户
        @param password: 密码
        @return: t.Union[OAuth2UserModel, None]

        注意: 密码模式只是兼容老版本而存在,特殊场景需求请重写依赖注入dependencies中的Oauth2或OpenID的setup方式注入自己的逻辑
        """
        raise NotImplementedError()

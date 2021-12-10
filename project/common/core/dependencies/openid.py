#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_authlib.core.dependencies.openid import OpenID as BaseOpenID
from project.common.core.server.common.grants.password import PasswordGrant


class OpenID(BaseOpenID):
    """ OpenID依赖类 """

    name = 'OpenID'

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param args  : 位置参数
        @param kwargs: 命名参数
        """
        super(OpenID, self).__init__(*args, **kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        super(OpenID, self).setup()
        self.server.register_grant(PasswordGrant, extensions=None)

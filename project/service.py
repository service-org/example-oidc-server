#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from service_consul.core.client import ConsulClient
from project.common.core.dependencies.openid import OpenID
from service_sqlalchemy.core.dependencies import SQLAlchemy
from service_prometheus.core.dependencies import Prometheus
from service_core.core.service import Service as BaseService
from service_consul.core.dependencies import ApiSixConsulKvRegist
from service_itsdangerous.core.client import URLSafeSerializerClient
from service_itsdangerous.core.dependencies import URLSafeSerializer
from service_authlib.core.server.common import OAuth2AuthorizationServer

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    name = 'oauth2'
    desc = 'Oauth2相关服务'

    prometheus = Prometheus(alias='prod')
    orm: SQLAlchemy = SQLAlchemy(alias='prod')
    consul: ConsulClient = ApiSixConsulKvRegist(alias='prod')
    openid_server: OAuth2AuthorizationServer = OpenID(alias='prod')
    cookie_serializer: URLSafeSerializerClient = URLSafeSerializer(alias='prod_cookie')

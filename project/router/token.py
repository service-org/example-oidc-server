#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from project.service import Service
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.response import Response
from service_webserver.core.entrypoints import webserver

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class OAuth2Token(Endpoint):
    """ OAuth2令牌 """

    @webserver.api('/token', methods=['POST'], tags=['oauth2'])
    def token(self, service: Service, request: Request) -> Response:
        """ 查询或更新OAuth2令牌

        @param service: 服务对象
        @param request: 请求对象
        @return: Response
        """
        return service.openid_server.create_token_response(request)

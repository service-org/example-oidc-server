#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import base64
import typing as t

from logging import getLogger
from project.service import Service
from itsdangerous.exc import BadData
from authlib.oauth2 import OAuth2Error
from project.models import OAuth2UserModel
from service_core.core.endpoint import Endpoint
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.response import Response
from service_webserver.core.entrypoints import webserver
from service_webserver.core.response import RedirectResponse
from service_sqlalchemy.core.shortcuts import safe_transaction

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class OAuth2Authorize(Endpoint):
    """ OAuth2授权 """

    @staticmethod
    def get_curr_url(request: Request) -> t.Text:
        """ 获取当前请求的地址

        @param request: 请求对象
        @return: t.Text
        """
        request_path = request.path
        query_string = request.query_string.decode('utf-8')
        return f'.{request_path}?{query_string}'

    def get_next_url(self, request: Request) -> t.Text:
        """ 获取登录认证的地址

        @param request: 请求对象
        @return: t.Text
        """
        url_string = self.get_curr_url(request)
        url_base64 = base64.b64encode(url_string.encode('utf-8')).decode('utf-8')
        return f'./login?next={url_base64}'

    @staticmethod
    def get_session_id(service: Service, request: Request) -> t.Union[t.Text, None]:
        """ 从请求对象中获取会话id

        @param service: 服务对象
        @param request: 请求对象
        @return: t.Text
        """
        session_id = request.cookies.get('session_id', default='')
        return service.cookie_serializer.loads(session_id)

    @webserver.web('/authorize', methods=['GET', 'POST'], tags=['oauth2'])
    def authorize(self, service: Service, request: Request) -> Response:
        """ 多种OAuth2授权请求处理

        @param service: 服务对象
        @param request: 请求对象
        @return: Response
        """
        next_url = self.get_next_url(request)
        try:
            session_id = self.get_session_id(service, request=request)
        except BadData:
            logger.error(f'unexpected error while unserializer session_id', exc_info=True)
            return RedirectResponse(next_url)
        with safe_transaction(service.orm, commit=False) as session:
            user = session.query(OAuth2UserModel).filter(OAuth2UserModel.id == session_id).first()
        if user is None:
            return RedirectResponse(next_url)
        try:
            service.openid_server.validate_consent_request(request, end_user=user)
        except OAuth2Error as error:
            logger.error(f'unexpected error while validate consent request', exc_info=True)
            return error.error
        return service.openid_server.create_authorization_response(request, grant_user=user)

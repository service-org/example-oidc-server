#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import base64
import typing as t

from logging import getLogger
from project.service import Service
from itsdangerous.exc import BadData
from project.models import OAuth2UserModel
from service_core.core.as_router import ApiRouter
from service_webserver.core.request import Request
from service_webserver.core.response import Response
from service_webserver.core.endpoint import Endpoint
from service_webserver.core.entrypoints import webserver
from service_webserver.core.response import HtmlResponse
from service_webserver.core.response import RedirectResponse
from service_sqlalchemy.core.shortcuts import safe_transaction

router = ApiRouter(__name__)
logger = getLogger(__name__)


@router()
class OAuth2Login(Endpoint):
    """ OAuth2登录 """

    entrypoint_wrapper = webserver.web
    entrypoint_options = {'raw_url': '/login', 'tags': ['oauth2']}

    @staticmethod
    def get_next_url(request: Request) -> t.Text:
        """ 获取请求授权的地址

        @param request: 请求对象
        @return: t.Text
        """
        url_base64 = request.args.get('next')
        return base64.b64decode(url_base64.encode('utf-8')).decode('utf-8')

    @staticmethod
    def get_session_id(service: Service, request: Request) -> t.Union[t.Text, None]:
        """ 从请求对象中获取会话id

        @param service: 服务对象
        @param request: 请求对象
        @return: t.Text
        """
        session_id = request.cookies.get('session_id', default='')
        return service.cookie_serializer.loads(session_id)

    @staticmethod
    def set_session_id(service: Service, response: Response, user_id: int) -> None:
        """ 设置会话id到响应对象

        @param service: 服务对象
        @param response: 响应对象
        @param user_id: 用户id
        @return: None
        """
        session_id = service.cookie_serializer.dumps(user_id)
        response.set_cookie('session_id', session_id)

    def get(self, service: Service, request: Request) -> Response:
        """ 渲染OAuth2登录页面

        @param service: 服务对象
        @param request: 请求对象
        @return: Response
        """
        response = '''
        <form action="" method="post">
            <label for="username">账户: </label>
            <input id="username" name="username" type="text"/><br>
            <label for="password">密码: </label>
            <input id="password" name="password" type="password"/><br>
            <button>登录</button>
        </form>
        '''
        return HtmlResponse(response)

    def post(self, service: Service, request: Request) -> Response:
        """ 处理OAuth2登录请求

        @param service: 服务对象
        @param request: 请求对象
        @return: Response
        """
        next_url = self.get_next_url(request)
        try:
            self.get_session_id(service, request=request)
            response = RedirectResponse(next_url)
        except BadData:
            logger.error(f'unexpected error while unserializer session_id', exc_info=True)
            username = request.form.get('username')
            password = request.form.get('password')
            # 此处请自行添加帐号密码验证逻辑,具体场景具体分析
            with safe_transaction(service.orm, commit=False) as session:
                user = session.query(OAuth2UserModel).filter(OAuth2UserModel.name == username).first()
            response = RedirectResponse(next_url)
            self.set_session_id(service, response=response, user_id=user.id)
        return response

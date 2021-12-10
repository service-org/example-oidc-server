#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project.router import token
from project.router import login
from project.router import authorize
from project.service import Service
from service_core.core.as_router import ApiRouter

router = ApiRouter(__name__)
router.include_router(token.router)
router.include_router(login.router)
router.include_router(authorize.router)

service = Service()
service.include_router(router)

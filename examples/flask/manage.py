#!/usr/bin/env python
# encoding: utf8
#
# Copyright © Anton Egorov <anton.egoroff@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    3. Neither the name of the owner nor the names of its contributors may be
#       used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

from werkzeug.middleware.dispatcher import DispatcherMiddleware

from spyne.server.wsgi import WsgiApplication
from spyne.protocol.soap import Soap11, Soap12
from apps import spyned
from apps.flasked import app


# SOAP services are distinct wsgi applications, we should use dispatcher
# middleware to bring all aps together
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/http_rpc': WsgiApplication(spyned.create_app(app)),
    '/soap_11': WsgiApplication(spyned.create_app(app, in_protocol=Soap11(), out_protocol=Soap11())),
    '/soap_12': WsgiApplication(spyned.create_app(app, in_protocol=Soap12(), out_protocol=Soap12())),
})


if __name__ == '__main__':
    app.run()

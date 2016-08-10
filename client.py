# -*- coding: utf-8 -*-
"""
    This file is part of the continuum IDA PRO plugin (see zyantific.com).

    The MIT License (MIT)

    Copyright (c) 2016 Joel Hoener <athre0z@zyantific.com>

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""
from __future__ import absolute_import, print_function, division

import asyncore
from idc import *
from idautils import *
from .proto import ProtoMixin


class Client(ProtoMixin, asyncore.dispatcher_with_send):
    def __init__(self, sock, core):
        asyncore.dispatcher_with_send.__init__(self, sock=sock)
        ProtoMixin.__init__(self)
        self.core = core
        self.become_host_on_dc = False
        self.idb_path = GetIdbPath()

        self.send_packet({
            'kind': 'new_client',
            'input_file': GetInputFile(),
            'idb_path': GetIdbPath(),
        })

        print("[continuum] Connected.")

    def handle_close(self):
        asyncore.dispatcher_with_send.handle_close(self)
        print("[continuum] Connection lost, reconnecting.")
        if self.become_host_on_dc:
            print("[continuum] We were elected as host.")
            self.core.create_server_if_none()
        self.core.create_client()

    def handle_msg_focus_symbol(self, symbol, **_):
        for i in xrange(GetEntryPointQty()):
            ordinal = GetEntryOrdinal(i)
            if GetEntryName(ordinal) == symbol:
                Jump(GetEntryPoint(ordinal))
                break

    def handle_msg_become_host(self, **_):
        self.become_host_on_dc = True
    
    def send_focus_symbol(self, symbol):
        self.send_packet({
            'kind': 'focus_symbol',
            'symbol': symbol,
        })

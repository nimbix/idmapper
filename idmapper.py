#
# Copyright (c) 2019, Nimbix, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nimbix, Inc.
#
import web
import os

urls = (
    '/map/(.*)', 'idmap'
)

app = web.application(urls, globals())


class idmap:
    ''' Provides the web service '''
    def GET(self, username):
        ''' Maps a username to an identity, if possible '''
        parts = username.split('@')
        domain = parts[1] if len(parts) > 1 else ''
        path = self.homepath.replace('%d', domain).replace(
            '%D', domain.upper()).replace(
                '%u', username if self.upnpath else parts[0])

        if os.path.exists(path):
            st = os.stat(path)
            return {'uid': st.st_uid,
                    'gid': st.st_gid,
                    'home': os.path.dirname(path)}
        else:
            return {}

    def __init__(self):
        ''' Constructor: stores configuration '''
        self.homepath = (os.environ.get('HOMEPATH', '/home/%u/'))
        self.upnpath = (os.environ.get('UPNPATH', 'false') == 'true')


if __name__ == '__main__':
    app.run()

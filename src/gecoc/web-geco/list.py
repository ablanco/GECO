# -*- coding: utf-8 -*-
import datetime
import web

from utils import authenticated, templated, flash, get_gso

session = web.ses

class list:
    render = web.template.render('templates')
    @authenticated
    @templated(css='style bootstrap',
            js='jquery-1.7.2.min bootstrap aes md5 sha256 gecojs masterkey list',
            menu=web.menu_user,
            title='GECO Web Client')
    def GET(self):
        username = session.get('username', '')
        cookie = session.get('gso', '')
        gso = get_gso(cookie=cookie)

        pwdlist = gso.get_all_passwords()
        def cmp(x, y):
            if x['name'] > y['name']: return 1
            else: return -1
        pwdlist.sort(cmp)
        # Cambiando el formato de la fecha
        for pwd in pwdlist:
            exp = pwd['expiration']
            expdate = datetime.datetime.fromtimestamp(float(exp))
            pwd['expiration'] = '%02d/%02d/%04d' % (expdate.day,
                    expdate.month, expdate.year)
            pwd['days'] = (expdate - datetime.datetime.now()).days

        body = self.render.index(username=username,
                pwdlist=pwdlist)

        return body

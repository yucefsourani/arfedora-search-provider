#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  arfedora-search-provider.py
#  
#  Copyright 2021 yucef sourni <youssef.m.sourani@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
import os
from urllib.request import urlopen,Request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import dbus
import dbus.service

from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib

class ArfedoraSearchProvider(dbus.service.Object):
    """The Arfedora Search daemon."""
    def __init__(self):
        """إنشاء خدمة dbus """
        self.session_bus = dbus.SessionBus()
        bus_name = dbus.service.BusName("org.gnome.Arfedora.SearchProvider", bus=self.session_bus)
        dbus.service.Object.__init__(self, bus_name, "/org/gnome/Arfedora/SearchProvider")
        self.result = {}

    @dbus.service.method(in_signature="as", out_signature="as", dbus_interface="org.gnome.Shell.SearchProvider2")
    def GetInitialResultSet(self, terms):
        # only parse queries that start with $ and contain 2 or more terms 
        """عند بحث المستخدم عن أي نص سيتم تمرير النص سيتم تقسيم السطر ووضعه في قائمة من الكلمات """
        self.result.clear()
        qs = "".join([t for t in terms]) # دمج كل الكلمات في سطر واحد والتخلي عن علامتي $
        qs = qs.strip()
        if len(qs) < 5 or not qs.startswith("$$"): # تأكد من أن المستخدم أدخل 3 أحرف على الأقل
            return []
        out = []
        try:
            url   = Request("https://arfedora.blogspot.com/search?{}&{}".format(urlencode({"q":qs[2:]}),urlencode({"max-results":"5"})),headers={"User-Agent":"Mozilla/5.0"})
            opurl = urlopen(url)
            soup  = BeautifulSoup(opurl,"html.parser")
            for h2 in soup.findAll("h2",{"class":"post-title entry-title"}):
                link_value  =  h2.a.get("href")
                title_value =  h2.a.text.strip()
                # سننحتاج قاموس يحتوي هذه المعلومات عن كل نتيجة ستظهر 
                self.result.setdefault(link_value,{"id": link_value,"name" : title_value[0:50] ,"description" : link_value ,"icon" :  "web-browser-symbolic"})
                out.append(link_value) # سنحتاج إرجاع قائمة بقيم مميزة لا تتكر لكل  نتيجة مثلا الرابط
        except Exception as e:
            print(e)
            pass
        return out

    @dbus.service.method(in_signature="asas", out_signature="as", dbus_interface="org.gnome.Shell.SearchProvider2")
    def GetSubsearchResultSet(self, previous_results, new_terms):
        return self.GetInitialResultSet(new_terms)

    @dbus.service.method(in_signature="as", out_signature="aa{sv}", dbus_interface="org.gnome.Shell.SearchProvider2")
    def GetResultMetas(self, ids):
        """ سيتم تشغيل هذه الوظيفة بعد إنتهاء GetInitialResultSet وسنحتاج هنا إرجاع قائمة بقواميس كل واحد يحتوي
        معلومة عن نتيجة ستظهر وممكن هنا توفير هذه المعلومات وإرجاعها لاكني قمب بهذا في الوظيفة السابقة وحفظتهم في result"""
        return self.result.values()

    @dbus.service.method(in_signature="sasu", dbus_interface="org.gnome.Shell.SearchProvider2")
    def ActivateResult(self, id, terms, timestamp):
        """ عند ضغط اامستخدم على النتيجة سيتم تنفيذ هذه الوظفية وسيتم إرسال القيمة المميزة لكل نتيجة ومنها يمكننا الوصول إلى description """
        link = self.result[id]["description"]
        os.system("xdg-open {}".format(link)) # بعد الحصول على الرابط قمت بفتحه من خلال اداة xdg-open
        
    @dbus.service.method(in_signature="asu", terms="as", timestamp="u", dbus_interface="org.gnome.Shell.SearchProvider2")
    def LaunchSearch(self, terms, timestamp):
        pass



if __name__ == "__main__":
    DBusGMainLoop(set_as_default=True)
    ArfedoraSearchProvider()
    GLib.MainLoop().run()
# رابط الوثائق
# https://developer.gnome.org/documentation/tutorials/search-provider.html

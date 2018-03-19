# -*- coding: utf-8 -*-

# Copyright(C) 2018      Gasselin Maxime
#
# This file is part of weboob.
#
# weboob is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# weboob is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with weboob. If not, see <http://www.gnu.org/licenses/>.

from __future__ import unicode_literals
from .browser import AccuweatherBrowser
from weboob.capabilities.weather import CapWeather, CityNotFound
from weboob.tools.backend import Module
from weboob.capabilities.base import find_object


__all__ = ['AccuweatherModule']


class AccuweatherModule(Module, CapWeather):
    NAME = 'accuweather'
    DESCRIPTION = u'accuweather website'
    MAINTAINER = u'Gasselin Maxime'
    EMAIL = 'm.gasselin@hotmail.fr'
    LICENSE = 'AGPLv3+'
    VERSION = '1.3'

    BROWSER = AccuweatherBrowser
    
    def get_current(self, _id):  
        return self.browser.get_current(_id)

    def iter_forecast(self, _id):  
        return self.browser.iter_forecast(_id)

    def iter_city_search(self, pattern):  
        return self.browser.iter_city_search(pattern)
    


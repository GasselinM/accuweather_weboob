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
from datetime import date
from weboob.browser.pages import JsonPage, HTMLPage
from weboob.browser.elements import ItemElement, ListElement, DictElement, method
from weboob.capabilities.base import NotAvailable
from weboob.capabilities.weather import Forecast, Current, City, Temperature
from weboob.browser.filters.json import Dict
from weboob.browser.filters.standard import CleanText, CleanDecimal, Regexp, Format, Eval

__all__ = ['SearchCitiesPage', 'WeatherPage']


class SearchCitiesPage(JsonPage):
    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            klass = City
            obj_id = Dict('Key')
            obj_name = Format(u'%s, State: %s, Country: %s', Dict('LocalizedName'), Dict['AdministrativeArea']['LocalizedName'], Dict['Country']['LocalizedName'])

class WeatherPage(HTMLPage):
    @method
    class iter_forecast(ListElement):
        item_xpath = '//div[@class="panel-body"]/div[@id="feed-tabs"]/ul/li'

        class item(ItemElement):
            klass = Forecast
            obj_id = CleanText('.//h3/a/text()')
            obj_date = CleanText('.//h4/text()')
            def obj_low(self):
                
                temp = CleanText('.//span[@class="small-temp"]/text()')(self)
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit= unit[-1]
                if temp.endswith('C') or temp.endswith('F'):
                    temp = temp[1:-2]
                elif temp == '':
                    temp = CleanText('//div[@class="night"]//span[@class="large-temp"]/text()')(self)
                    temp = temp[:-1]                    
                else:
                    temp = temp[1:-1]
                return Temperature(float(temp), unit)

            def obj_high(self):
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit= unit[-1]
                if CleanText('.//span[@class="small-temp"]/text()')(self) == '':
                    temp = CleanText('//div[@id="detail-day-night"]//div[@class="info"]//span[@class="large-temp"]/text()')(self)
                    temp = temp[:-1]
                    return Temperature(float(temp), unit)
                temp = CleanText('.//span[@class="large-temp"]/text()')(self)                
                temp = temp[:-1]
                return Temperature(float(temp), unit)

            obj_text = CleanText('.//span[@class="cond"]/text()')

    @method
    class get_current(ItemElement):
        klass = Current
        #obj_id = date.today()
        obj_date = date.today()
        
        obj_text = Format('Real feel %sC - %s - UV %s - Wind < %s',
                          CleanText('//div[@class="lt"]//tbody/tr[3]/td/text()'),
                          CleanText('//div[@id="detail-now"]//div[@class="forecast"]//span[@class="cond"]/text()'),
                          CleanText('//div[@id="detail-now"]//li[5]/strong/text()'),                          
                          CleanText('//li[@class="wind"]/strong/text()'))

        def obj_temp(self):            
            temp = CleanText('//div[@class="lt"]//tbody/tr[1]/td/text()')(self)
            temp = temp[:-1]
            unit = CleanText('//div[@class="lt"]//thead/tr/th/text()[1]')(self)
            unit = unit[-2]
            return Temperature(float(temp), unit)
            #2018-03-13: 10 °C - Ressenti 10°C - Éclaircies - UV 1 - Vent < 5 km/h
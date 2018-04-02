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
from weboob.browser.filters.standard import CleanText, Format

__all__ = ['SearchCitiesPage', 'WeatherPage']


class SearchCitiesPage(JsonPage):
    """ Use of the accuweather API to scrap informations 
    about cities and their ID for accuweather reasearch"""
    @method
    class iter_cities(DictElement):
        ignore_duplicate = True

        class item(ItemElement):
            """obj_id help to consctuct the good url where to connect;
            obj_name, informations for the user to help him to do the good choice"""
            klass = City
            obj_id = Dict('Key')
            obj_name = Format(u'%s, State: %s, Country: %s', Dict('LocalizedName'), Dict['AdministrativeArea']['LocalizedName'], Dict['Country']['LocalizedName'])

class WeatherPage(HTMLPage):
    @method
    class get_current(ItemElement):
        """Method to get informations about current weather
        The result will be format like this: 
        2018-03-13: 10 °C - Ressenti 10°C - Éclaircies - UV 1 - Vent < 5 km/h"""
        klass = Current
        obj_date = date.today()
        #Scrapping of the supplemental informations 
        obj_text = Format('Real feel %sC - %s - UV %s - Wind < %s',
                          CleanText('//div[@class="lt"]//tbody/tr[3]/td/text()'),
                          CleanText('//div[@id="detail-now"]//div[@class="forecast"]//span[@class="cond"]/text()'),
                          CleanText('//div[@id="detail-now"]//li[5]/strong/text()'),                          
                          CleanText('//li[@class="wind"]/strong/text()'))

        def obj_temp(self):
            """Scrapping of the temperature 
            and its unit"""
            temp = CleanText('//div[@class="lt"]//tbody/tr[1]/td/text()')(self)
            temp = temp[:-1]
            unit = CleanText('//div[@class="lt"]//thead/tr/th/text()')(self)
            unit = unit[-2]
            return Temperature(float(temp), unit)
    
    @method
    class iter_forecast(ListElement):
        """Method to get informations about forecasts weather
        The result will be format like this (for one day): 
        Apr 2:          (11 °C - 16 °C) Rain and drizzle this evening"""
        #item to iter for each day
        item_xpath = '//div[@class="panel-body"]/div[@id="feed-tabs"]/ul/li'

        class item(ItemElement):
            klass = Forecast
            #Day of the week
            obj_id = CleanText('.//h3/a/text()')
            #Calendar day
            obj_date = CleanText('.//h4/text()')

            def obj_low(self):
                """Scrapping of the minimal temperature 
                (and its unit) of the day"""      
                temp = CleanText('.//span[@class="small-temp"]/text()')(self)
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit= unit[-1]
                if temp.endswith('C') or temp.endswith('F'):
                    #temp is like /x°C
                    temp = temp[1:-2]
                elif temp == '':
                    #When it's night the first day is empty                 
                    temp = CleanText('//div[@class="night"]//span[@class="large-temp"]/text()')(self)
                    temp = temp[:-1]                     
                else:
                    #temp is like /27°
                    temp = temp[1:-1]
                return Temperature(float(temp), unit)

            def obj_high(self):
                """Scrapping of the maximal temperature 
                (and its unit) of the day"""
                unit= CleanText('//span[@class="local-temp"]/text()')(self)
                unit= unit[-1]
                if CleanText('.//span[@class="small-temp"]/text()')(self) == '':
                    #When it's night the first day is empty 
                    temp = CleanText('//div[@id="detail-day-night"]//div[@class="info"]//span[@class="large-temp"]/text()')(self)
                    temp = temp[:-1]
                    return Temperature(float(temp), unit)
                temp = CleanText('.//span[@class="large-temp"]/text()')(self)                
                temp = temp[:-1]
                return Temperature(float(temp), unit)

            obj_text = CleanText('.//span[@class="cond"]/text()')


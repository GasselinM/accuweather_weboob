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


from weboob.tools.test import BackendTest


class AccuweatherTest(BackendTest):
    MODULE = 'accuweather'

    def testAccuweatherSearch(self):
        """ Check if Search tool return good
        number of city"""
        
        l = list(self.backend.iter_city_search('Paris'))
        # Is Paris search return more than 9 results ?
        self.assertTrue(len(l) > 9)

        k = list(self.backend.iter_city_search('Graveson'))
        # Is Graveson search return one city ?
        self.assertTrue(len(k) == 1)        

        
    def testAccuweatherCurrent(self):
        """Check if "Current" tool return consistent 
        temperatures for Paris"""
        l = list(self.backend.iter_city_search('Paris'))
        city = l[0]
        current = self.backend.get_current(city.id)
        
        # Check if the unit are well-scraped
        self.assertTrue(current.temp.unit in ['C', 'F'])
        
        # Check if the temperatures is consistent (i hope that global warming doesn't break this test...)
        if current.temp.unit == 'C':
            self.assertTrue(current.temp.value > -20 and current.temp.value < 50)        
        elif current.temp.unit == 'F':
            self.assertTrue(current.temp.value > -4 and current.temp.value < 130)

    def testAccuweatherForecasts(self):        
        """Check if "Forecasts" tool return consistent 
        values for Paris"""
        l = list(self.backend.iter_city_search('Paris'))
        city = l[0]
        forecasts = list(self.backend.iter_forecast(city.id))
        
        # Check if forecasts return values for 5 days
        self.assertTrue(len(forecasts) == 5)
        
        # Check if unit is well-scraped and temperatures consistent
        for forecast in forecasts:
            for j in [forecast.high, forecast.low]:
                self.assertTrue(j.unit in ['C', 'F'])
                if j.unit == 'C':
                    self.assertTrue(j.value > -20 and j.value < 50)        
                elif j.unit == 'F':
                    self.assertTrue(j.value > -4 and j.value < 130)
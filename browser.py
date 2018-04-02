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
from weboob.browser import PagesBrowser, URL
from .pages import WeatherPage, SearchCitiesPage

__all__ = ['AccuweatherBrowser']

class AccuweatherBrowser(PagesBrowser):
    """ URLs where to scrap elements, with the 
    help of Accuweather's API"""
    cities = URL('https://api.accuweather.com/locations/v1/cities/autocomplete\?q=(?P<pattern>.*)&apikey=d41dfd5e8a1748d0970cba6637647d96&language=en-us&get_param=value', SearchCitiesPage)
    weather = URL('https://www.accuweather.com/en/fr/city/(?P<city_id1>.*)/current-weather/(?P<city_id2>.*)',  WeatherPage)
    forecast = URL('https://www.accuweather.com/en/fr/city/(?P<city_id1>.*)/daily-weather-forecast/(?P<city_id2>.*)', WeatherPage)
    
    def iter_city_search(self, pattern):
        """Method to connect with the API 
        with the city of choice"""
        return self.cities.go(pattern=pattern).iter_cities()

    def get_current(self, _id):
        """Method to connect with the accuweather 
        website with the Curent tool"""
        self.weather.go(city_id1=_id,city_id2=_id)
        return self.page.get_current()

    def iter_forecast(self, _id):
        """Method to connect with the accuweather
        website with the Forecasts tool"""
        self.forecast.go(city_id1=_id,city_id2=_id)
        return self.page.iter_forecast()

    
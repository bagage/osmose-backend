#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Adrien Pavie 2017                                          ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from Analyser_Merge import Analyser_Merge, Source, JSON, Load, Mapping, Select, Generate


class Analyser_Merge_Public_Equipment_FR_Montpellier_Toilets(Analyser_Merge):
    def __init__(self, config, logger = None):
        self.missing_official = {"item":"8180", "class": 6, "level": 3, "tag": ["merge", "public equipment"], "desc": T_(u"%s toilets not integrated", "Montpellier") }
        Analyser_Merge.__init__(self, config, logger,
            "http://data.montpellier3m.fr/dataset/toilettes-publiques-de-montpellier",
            u"Toilettes publiques",
            JSON(Source(attribution = u"Montpellier Mediterranée Métropole", millesime = "12/2017",
                    fileUrl = "http://data.montpellier3m.fr/sites/default/files/ressources/MMM_MTP_WC_PUBLICS.json", encoding = "ISO-8859-15"),
                extractor = lambda json: json['features']),
            Load("geometry.x", "geometry.y",
                select = {u'attributes.enservice': u'"En Service"'}),
            Mapping(
                select = Select(
                    types = ["nodes", "ways"],
                    tags = {"amenity": "toilets"}),
                conflationDistance = 100,
                generate = Generate(
                    static1 = {
                        "amenity": "toilets",
                        "access": "public"},
                    static2 = {"source": self.source},
                    mapping1 = {
                        "name": lambda res: res['attributes.nom'].replace('"', '') if res['attributes.nom'] else None,
                        "operator": lambda res: res['attributes.gestion'].replace('"', '') if res['attributes.gestion'] else None,
                        "wheelchair": lambda res: "yes" if res['attributes.pmr'] == u'"PMR"' else "no" if res['attributes.pmr'] == u'"non PMR"' else None } )))

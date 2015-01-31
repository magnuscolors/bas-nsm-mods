# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright 2014 BAS Solutions
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "NSM Betaalherinnering layout",
    "version": "2.0",
    "author": "BAS Solutions",
    "website": "https://www.bas-solutions.nl",
    "category": "Sales Management",
    "depends": ["base", "account_followup"],
    "summary": "New Skool Media Betaalherinnering layout",
    "description": """
    New Skool Media Betaalherinnering layout
    """,
    'images': [
               ],
    "init_xml": [
                 ],
    "update_xml": [
             "payment_followup_report.xml"
        ],
    'demo_xml': [
    ],
    'test':[
    ],
    'installable': True,
    'auto_install': False,
    'application':False
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

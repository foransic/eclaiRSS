#!/usr/bin/python

import requests
import json
import xml.etree.ElementTree as ET

# we set JSON data
requestMetadata = {'marketplaceID' : 'A13V1IB3VIYZZH' , 'clientID' : 'goldbox'}

dealMetadata = {
	'requestMetadata': requestMetadata,
	'widgetContext' : {'pageType' : 'Landing','subPageType' : 'hybrid-batch-atf','deviceType' : 'pc','refRID' : '0C4CPSGQHXY6JSW0ER2M','widgetID' : '653378407','slotName' : 'merchandised-search-2'},
	'page' : 1,	'dealsPerPage':20, 'itemResponseSize' : 'NONE',
	'queryProfile':{'featuredOnly':'false','inclusiveTargetValues':[{'name' : 'MARKETING_ID','value' : 'eclair'}],'excludedExtendedFilters':{'MARKETING_ID':['Kindle']}}
}

headers = {'Content-type' : 'application/json'}

# first call -> get deal list
metadataRequest = requests.post('http://www.amazon.fr/xa/dealcontent/v2/GetDealMetadata', data=json.dumps(dealMetadata), headers=headers)

jsonMetadata = metadataRequest.json();
dealTargets = []

for dealId in jsonMetadata['dealsByState']['AVAILABLE']:
	dealTargets.append({"dealID" : dealId})

dealsData = {
	'requestMetadata': requestMetadata,
	'dealTargets' : dealTargets,
	'responseSize' : 'ALL',
	'itemResponseSize' : 'NONE'
};

# second call -> get available deal details & create RSS
dealsRequest = requests.post('http://www.amazon.fr/xa/dealcontent/v2/GetDeals', data=json.dumps(dealsData), headers=headers)

jsonDeals = dealsRequest.json();

rssItems = []

rss = ET.Element('rss')
rss.set('version', '2.0')
channel = ET.SubElement(rss, 'channel')
ET.SubElement(channel, 'title').text = 'Offres Eclair'
ET.SubElement(channel, 'description').text = 'Les offres Eclair Amazon dans votre feed RSS'

for dealId in jsonDeals['dealDetails']:
	deal = jsonDeals['dealDetails'][dealId]
	
	item = ET.SubElement(channel, 'item')
	ET.SubElement(item, 'title').text = deal['title']
	ET.SubElement(item, 'link').text = 'http://www.amazon.fr/gp/product/' + deal['impressionAsin']
	ET.SubElement(item, 'description').text = deal['title'] + ' - ' + str(deal['minDealPrice']) + u"\u20AC"

tree = ET.ElementTree(rss)

print "Content-type: application/rss+xml\n\n"

ET.dump(tree.getroot())


#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom


def parse_file(filename):
	result = {'2.4Ghz':[],'5Ghz':[]}
	DOMTree = xml.dom.minidom.parse(filename)
	gpx = DOMTree.documentElement
	wpts = gpx.getElementsByTagName('wpt')
	for wpt in wpts:
		wpt_struct = {}
		if wpt.hasAttribute("lat") and wpt.hasAttribute("lon"):
			wpt_struct.update({'lat': wpt.getAttribute("lat"), 'lon': wpt.getAttribute("lon")})
		wpt_ext = wpt.getElementsByTagName("extensions")[0].getElementsByTagName('*')
		for item in wpt.getElementsByTagName("*"):
			if item.tagName == "extensions":
				wpt_struct['extensions'] = {}
				for ext in item.getElementsByTagName("*"):
					wpt_struct['extensions'][ext.tagName] = ext.childNodes[0].data
			else:
				if len(item.childNodes)>0:
					wpt_struct[item.tagName] = item.childNodes[0].data
		print wpt_struct['ChannelID']
		if int(wpt_struct['ChannelID'])<15:
			result['2.4Ghz'].append(wpt_struct)
		else:
			result['5Ghz'].append(wpt_struct)
	return result




FiveGhz=[]
TwodotfourGhz=[]

cur_file = "./testdata/1.gpx"
results=parse_file(cur_file)
print results['2.4Ghz'][0]['desc']


#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom
import os
import argparse


def split_wifi_xml(filename,output_filebase=None):
	result = {'2.4Ghz':[],'5Ghz':[]}
	if output_filebase:
		impl = xml.dom.minidom.getDOMImplementation()
		xml2_4 = impl.createDocument(None, "gpx", None)
		xml5 = impl.createDocument(None, "gpx", None)
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
		if int(wpt_struct['ChannelID'])<15:
			result['2.4Ghz'].append(wpt_struct)
			if output_filebase:
				xml2_4.firstChild.appendChild(wpt)
		else:
			result['5Ghz'].append(wpt_struct)
			if output_filebase:
				xml5.firstChild.appendChild(wpt)
	if output_filebase:
		f1 = open(output_filebase+'_2_4.xml','w+')
		f2 = open(output_filebase+'_5.xml','w+')
		f1.write(xml2_4.toxml('utf-8'))
		f2.write(xml5.toxml('utf-8'))
		f1.close()
		f2.close()
	return result

# Arguments hadnling
parser = argparse.ArgumentParser(description='Parse GPX files in directore <dir> \
											and splits output to 2,4Ghz and 5Ghz')
parser.add_argument('directory', metavar='<dir>', type=str, nargs=1, help='directory, where to search for GPX files')
parser.add_argument('--xml',metavar='<filename_base>',type=str,help='Create output xml files')
args = parser.parse_args()
directory = args.directory[0]
xml_output = args.xml
#Result init
results={'2.4Ghz':[],'5Ghz':[]}

# Main
for file in os.listdir(directory):
	if file.endswith(".gpx"):
		result=split_wifi_xml(directory+file,xml_output) #Parse file
		results['2.4Ghz']+=result['2.4Ghz'] # Append 2.4 part to results
		results['5Ghz']+=result['5Ghz'] # Append 5 Ghz part to results
		# Code needed to Display results in selected format





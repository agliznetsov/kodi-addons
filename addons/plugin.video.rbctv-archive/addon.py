#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import urllib
import urlparse
import time

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from rbc import RbcClient


def buildUrl(query):
    return baseUrl + '?' + urllib.urlencode(query)


def addItem(text1, url, isFolder):
    li = xbmcgui.ListItem(text1)
    xbmcplugin.addDirectoryItem(handle=addonHandle, url=url, listitem=li, isFolder=isFolder)


def root():
    li = xbmcgui.ListItem('[COLOR red]' + '[Favorites]' + '[/COLOR]')
    xbmcplugin.addDirectoryItem(handle=addonHandle, url=buildUrl({'mode': 'favorites'}), listitem=li, isFolder=True)

    li = xbmcgui.ListItem('[Programs]')
    xbmcplugin.addDirectoryItem(handle=addonHandle, url=buildUrl({'mode': 'programs'}), listitem=li, isFolder=True)


def programs():
    for it in client.programs():
        addItem(it['text'], buildUrl({'path': it['path'], 'mode': 'folder'}), True)


def folder(path):
    for it in client.issues(path):
        li = xbmcgui.ListItem(it['text'])
        li.setProperty('IsPlayable', 'true')
        url = buildUrl({'path': it['path'], 'mode': 'file', 'text': it['text'].encode('utf-8')})
        xbmcplugin.addDirectoryItem(handle=addonHandle, url=url, listitem=li, isFolder=False)


def favorites():
    fav = addon.getSetting('favorites')
    favorites = fav.split(' ')
    for f in favorites:
        addItem(f, buildUrl({'path': '/archive/' + f, 'mode': 'folder'}), True)


def news():
    playlist = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
    xbmc.PlayList.clear(playlist)
    for it in client.favorites():
        addItem(it['text'], it['path'], False)
        li = xbmcgui.ListItem(label=it['text'], path=it['path'])
        playlist.add(it['path'], li)
        # xbmc.Player().play(playlist)
    xbmcplugin.setResolvedUrl(addonHandle, True, playlist[0])


def file(text, path):
    it = client.file(path)
    li = xbmcgui.ListItem(label=text, path=it['path'])
    xbmcplugin.setResolvedUrl(addonHandle, True, li)
    # addItem(it['path'], it['path'], False)


baseUrl = sys.argv[0]
addonHandle = int(sys.argv[1])
query = sys.argv[2]

xbmcplugin.setContent(addonHandle, 'movies')
args = urlparse.parse_qs(query[1:])
path = args.get('path', [None])[0]
text = args.get('text', [''])[0].decode('utf-8')
mode = args.get('mode', ['root'])[0]

addon = xbmcaddon.Addon(id='plugin.video.rbctv-archive')
client = RbcClient()
start_time = time.time()

if mode == 'root':
    root()
elif mode == 'favorites':
    favorites()
elif mode == 'programs':
    programs()
elif mode == 'folder':
    folder(path)
else:
    file(text, path)

elapsed_time = time.time() - start_time
print 'finished in %s' % (elapsed_time)

xbmcplugin.endOfDirectory(addonHandle)

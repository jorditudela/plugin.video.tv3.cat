#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import re
import urlparse
import xbmc
import xbmcplugin
import xbmcaddon
import xbmcgui
import urllib
import urllib2
import json
import math
import time


#Localized strings
t_avuidestaquem=30001
t_noperdis=30002
t_mesvist=30003
t_programes=30004
t_series=30005
t_informatius=30006
t_entreteniment=30007
t_esports=30008
t_documentals=30009
t_divulgacio=30010
t_cultura=30011
t_musica=30012
t_tots=30013
t_emissio=30014
t_seguent=30015
t_anterior=30016
t_directe=30017
t_tv3=30018
t_canal324=30019
t_c33super3=30020
t_esport3=30021


url_base = 'http://www.ccma.cat'
url_alacarta = 'http://www.ccma.cat/tv3/alacarta/'
url_coleccions = 'http://www.ccma.cat/tv3/alacarta/coleccions/'
url_mesvist = 'http://www.ccma.cat/tv3/alacarta/mes-vist/'
url_datavideos = 'http://dinamics.ccma.cat/pvideo/media.jsp?media=video&version=0s&idint='
url_programes_emisio = 'http://www.ccma.cat/tv3/alacarta/programes'
url_programes_tots = 'http://www.ccma.cat/tv3/alacarta/programes-tots/'
urlZonaZaping = 'http://www.ccma.cat/tv3/alacarta/zona-zaping/'
urlApm = 'http://www.ccma.cat/tv3/alacarta/apm/'
url_directe_tv3 = 'http://ccma-tva-es-abertis-live.hls.adaptive.level3.net/es/ngrp:tv3_web/playlist.m3u8'
url_directe_324 = 'http://ccma-tva-int-abertis-live.hls.adaptive.level3.net/int/ngrp:324_web/playlist.m3u8'
url_directe_c33s3 = 'http://ccma-tva-es-abertis-live.hls.adaptive.level3.net/es/ngrp:c33_web/playlist.m3u8'
url_directe_esport3 = 'http://ccma-tva-es-abertis-live.hls.adaptive.level3.net/es/ngrp:es3_web/playlist.m3u8'

addon = xbmcaddon.Addon()
addon_path = xbmc.translatePath(addon.getAddonInfo('path'))

def index():
    xbmc.log( "--------------index------------------")
    
    
    addDir(addon.getLocalizedString(t_avuidestaquem).encode("utf-8"),"","destaquem","")
    addDir(addon.getLocalizedString(t_noperdis).encode("utf-8"),"","noperdis","")
    addDir(addon.getLocalizedString(t_mesvist).encode("utf-8"),"","mesvist","")
    addDir(addon.getLocalizedString(t_programes).encode("utf-8"),"","programes","")
    addDir(addon.getLocalizedString(t_directe).encode("utf-8"),"","directe","")
    
    xbmcplugin.endOfDirectory(addon_handle)
    
def listDestaquem():
    xbmc.log("--------------listDestaquem----------")
    
    
    #featured video
    html_destacats = getUrl(url_alacarta)
    match = re.compile('<div class="subitem destacat">[^<]+<a.+?href="(.+?)"').findall(html_destacats)
    if len(match) > 0:
        c = match[0]
        code = c[-8:-1]
  
        html_data = getUrl(url_datavideos + code + '&profile=pc')

        html_data = html_data.decode("ISO-8859-1")
        data =json.loads(html_data)
        
        if len(data) > 0:
            addLink(data)
   
    #more videos
    match = re.compile('<div class="subitem R-petit">[^<]+<a.+?href="(.+?)"').findall(html_destacats)

    for c in match:
       
        code = c[-8:-1]
        
        xbmc.log( "--------CODIS VIDEOS------------")
        xbmc.log( "codi: " + code)
        xbmc.log( "url: " + url_datavideos + code + '&profile=pc')
    
        html_data = getUrl(url_datavideos + code + '&profile=pc')
        
        html_data = html_data.decode("ISO-8859-1")
        data =json.loads(html_data)
        
        if len(data) > 0:
            addLink(data)
            
    xbmcplugin.endOfDirectory(addon_handle)
    
    
def listNoPerdis():
    xbmc.log("--------------listNoPerdis----------")
    
    link = getUrl(url_coleccions)
    match = re.compile('<li class="sensePunt R-elementLlistat  C-llistatVideo">[^<]+<a.+?href="(.+?)"').findall(link)

    for c in match:
        code = c[-8:-1]
        
        link = getUrl(url_datavideos + code + '&profile=pc')
        
        link = link.decode("ISO-8859-1")
        data =json.loads(link)
        
        if len(data) > 0:
            addLink(data)
        
    xbmcplugin.endOfDirectory(addon_handle) 
        
def listMesVist():
   
    link = getUrl(url_mesvist)
    match = re.compile('<li class="sensePunt R-elementLlistat  C-llistatVideo">.+?<small class="avantitol">.+?</small><h3 class="titol"><a href="(.+?)"').findall(link)

    for c in match:
        code = c[-8:-1]
        
        link = getUrl(url_datavideos + code + '&profile=pc')
       
        link = link.decode("ISO-8859-1")
        data =json.loads(link)
        
        if len(data) > 0:
            addLink(data)
        
    xbmcplugin.endOfDirectory(addon_handle)
    
def dirSections():
   
    addDir(addon.getLocalizedString(t_series).encode("utf-8"),"/series/","sections","")
    addDir(addon.getLocalizedString(t_informatius).encode("utf-8"),"/informatius/","sections","")
    addDir(addon.getLocalizedString(t_entreteniment).encode("utf-8"),"/entreteniment/","sections","")
    addDir(addon.getLocalizedString(t_esports).encode("utf-8"),"/esports/","sections","")
    addDir(addon.getLocalizedString(t_documentals).encode("utf-8"),"/documentals/","sections","")
    addDir(addon.getLocalizedString(t_divulgacio).encode("utf-8"),"/divulgacio/","sections","")
    addDir(addon.getLocalizedString(t_cultura).encode("utf-8"),"/cultura/","sections","")
    addDir(addon.getLocalizedString(t_musica).encode("utf-8"),"/musica/","sections","")
    addDir(addon.getLocalizedString(t_emissio).encode("utf-8"),"","dirAZemisio","")
    addDir(addon.getLocalizedString(t_tots).encode("utf-8"),"","dirAZtots","")
    
   
    xbmcplugin.endOfDirectory(addon_handle)
    
def listSections(url):
  
    link = getUrl(url_programes_emisio + url)
    match = re.compile('<ul class="R-abcProgrames">[\s\S]*?</ul>').findall(link)
    
    
    
    for i in match:
        d = re.compile('<li><a href="(.+)">(.+)</a></li>').findall(i)
        for program in d:
            url = program[0]
            titol = program[1]
            
            #test url
            urlProg = url_base + url
            if urlProg == urlApm or urlProg == urlZonaZaping:
                    url_final = urlProg + 'clips/'
            else:
                match = re.compile('(http://www.ccma.cat/tv3/alacarta/.+?/fitxa-programa/)(\d+/)').findall(urlProg)
                if len(match) <> 0:
                    url1 = match[0][0]
                    urlcode = match[0][1]
                    url_final = url1 + 'ultims-programes/' + urlcode
                else:
                    url_final = urlProg + 'ultims-programes/'
            
            addDir(titol,url_final,'listvideos', "")
        
    xbmcplugin.endOfDirectory(addon_handle) 
    
def listDirecte():
  
    thumb_tv3 = os.path.join(addon_path, 'resources', 'media', 'tv3_thumbnail.png')
    thumb_324 = os.path.join(addon_path, 'resources', 'media', '324_thumbnail.png')
    thumb_c33s3 = os.path.join(addon_path, 'resources', 'media', 'c33-super3_thumbnail.png')
    thumb_esp3 = os.path.join(addon_path, 'resources', 'media', 'esports3_thumbnail.png')
 
    listTV3 = xbmcgui.ListItem(addon.getLocalizedString(t_tv3).encode("utf-8"), iconImage=thumb_tv3,  thumbnailImage=thumb_tv3)
    listTV3.setProperty('isPlayable','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=url_directe_tv3,listitem=listTV3)
    
    list324 = xbmcgui.ListItem(addon.getLocalizedString(t_canal324).encode("utf-8"), iconImage=thumb_324,  thumbnailImage=thumb_324)
    list324.setProperty('isPlayable','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=url_directe_324,listitem=list324)
    
    listC33S3 = xbmcgui.ListItem(addon.getLocalizedString(t_c33super3).encode("utf-8"), iconImage=thumb_c33s3,  thumbnailImage=thumb_c33s3)
    listC33S3.setProperty('isPlayable','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=url_directe_c33s3,listitem=listC33S3)
    
    listEsport3 = xbmcgui.ListItem(addon.getLocalizedString(t_esport3).encode("utf-8"), iconImage=thumb_esp3,  thumbnailImage=thumb_esp3)
    listEsport3.setProperty('isPlayable','true')
    xbmcplugin.addDirectoryItem(handle=addon_handle,url=url_directe_esport3,listitem=listEsport3)
        
    xbmcplugin.endOfDirectory(addon_handle) 
    
def dirAZ_emisio():
  
    addDir("A-C","#A-C","listAZemisio","")
    addDir("D-E","D-E","listAZemisio","")
    addDir("H-I","H-I","listAZemisio","")
    addDir("J-L","J-L","listAZemisio","")
    addDir("M-P","M-P","listAZemisio","")
    addDir("Q-S","Q-S","listAZemisio","")
    addDir("T-V","T-V","listAZemisio","")
    addDir("X-Z","X-Z","listAZemisio","")
    
    xbmcplugin.endOfDirectory(addon_handle)
    
def dirAZ_tots():

    addDir("A-C","#A-C","listAZtots","")
    addDir("D-E","D-E","listAZtots","")
    addDir("H-I","H-I","listAZtots","")
    addDir("J-L","J-L","listAZtots","")
    addDir("M-P","M-P","listAZtots","")
    addDir("Q-S","Q-S","listAZtots","")
    addDir("T-V","T-V","listAZtots","")
    addDir("X-Z","X-Z","listAZtots","")
    
    xbmcplugin.endOfDirectory(addon_handle)
    
def listProgramesAZ(url, letters):
  
    r = '<div class="M-separadorSeccio"><h1 class="titol">[' + letters + ']</h1></div>\s*<ul class="R-abcProgrames">[\s\S]*?</ul>'
    
    link = getUrl(url)
    match = re.compile(r).findall(link)
    
    
    
    for i in match:
        d = re.compile('<li><a href="(.+)">(.+)</a></li>').findall(i)
        for program in d:
            url = program[0]
            titol = program[1]
            
            #test url
            urlProg = url_base + url
            
            if urlProg == urlApm or urlProg == urlZonaZaping:
                    url_final = urlProg + 'clips/'
            else:
                match = re.compile('(http://www.ccma.cat/tv3/alacarta/.+?/fitxa-programa/)(\d+/)').findall(urlProg)
                if len(match) <> 0:
                    url1 = match[0][0]
                    urlcode = match[0][1]
                    url_final = url1 + 'ultims-programes/' + urlcode
                else:
                    url_final = urlProg + 'ultims-programes/'
            
            addDir(titol,url_final,'listvideos', "")
        
    xbmcplugin.endOfDirectory(addon_handle) 
    
def listVideos(url):
   
    xbmc.log('Url listvideos: ' + url)
    link = getUrl(url)
    
    match = re.compile('<li class="F-llistat-item">[^<]*<a.+?href="(.+?)">').findall(link)
   
    if len(match) <> 0: 
    
        #test code
        url_test = match[0]
        test = re.compile('/tv3/alacarta/.+?/([0-9]{7})').findall(url_test)
        if len(test) < 1:
            match = re.compile('<article class="M-destacat.+?">[^<]*<a.+?href="(.+?)" title=".+?">').findall(link)
        
        
        if len(match) <> 0:
        
            for c in match:
                
                code = c[-8:-1]
                data = getDataVideo(url_datavideos + code + '&profile=pc')
                    
                if data <> None and len(data) > 0:
                    addLink(data)
                
               
            #Pagination
            match = re.compile('<p class="numeracio">P\xc3\xa0gina (\d+) de (\d+)</p>').findall(link)
            if len(match) <> 0:
                actualPage = int(match[0][0])
                totalPages = int(match[0][1])
                
                if actualPage < totalPages:
                    nextPage = str(actualPage + 1)
                    url_next = url + '?text=&profile=&items_pagina=15&pagina=' + nextPage
                    addDir(addon.getLocalizedString(t_seguent).encode("utf-8"), url_next, "listvideos", "")
                    
            xbmcplugin.endOfDirectory(addon_handle)
            
    
def addDir(name, url, mode,iconimage):
    u = build_url({'mode':mode,'name':name,'url':url})
    liz = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"title":name})
    ok = xbmcplugin.addDirectoryItem(handle=addon_handle,url=u,listitem=liz,isFolder=True)
    return ok
    
def addLink(data):
    ok = True
   
    linkvideo = None
    media = data.get('media',{})
    
    if type(media) is list and len(media) > 0:
        media_dict = media[0]
        linkvideo = media_dict.get('url', None)
    else:
        linkvideo = media.get('url', None)
        
    if linkvideo <> None:
        titol = data.get('informacio',{}).get('titol', None)
        image = data.get('imatges',{}).get('url', None)
        descripcio = data.get('informacio',{}).get('descripcio', None)
        programa = data.get('informacio',{}).get('programa', None)
        capitol = data.get('informacio',{}).get('capitol', None)
        tematica = data.get('informacio',{}).get('tematica',{}).get('text', None)
        data_emisio = data.get('informacio',{}).get('data_emissio',{}).get('text', None)
        milisec = data.get('informacio',{}).get('durada', {}).get('milisegons', None)
        durada = ""
        
        if milisec <> None:
            durada = milisec/1000
        
        liz = xbmcgui.ListItem(titol, iconImage="DefaultVideo.png", thumbnailImage=image)
        
        if descripcio == None:
            descripcio = ''       
            
        if programa <> None:
            if type(programa) is int or type(programa) is float:
                programa = str(programa)
            descripcio = '[B]' + programa + '[/B]' + '[CR]' + descripcio
            
           
        infolabels = {}
        
        if titol <> None:
            infolabels['title'] = titol
            xbmc.log('Titol: ' + titol.encode("utf-8"))
            
        if capitol <> None:
            infolabels['episode'] = capitol
            xbmc.log('Capitol: ' + str(capitol))
            
        if descripcio <> None:
            infolabels['plot'] = descripcio
          
        if tematica <> None:
            infolabels['genre'] = tematica
           
        if data_emisio <> None:
            dt = data_emisio[0:10]
            year = data_emisio[6:10]
            infolabels['aired'] = dt
            infolabels['year'] = year
          
        liz.setInfo('video', infolabels)
        liz.addStreamInfo('video',{'duration':durada})
        liz.setProperty('isPlayable','true')
        ok = xbmcplugin.addDirectoryItem(handle=addon_handle,url=linkvideo,listitem=liz)
        
    else:
        ok = None
    return ok
  
def build_url(query):
	return base_url + '?' + urllib.urlencode(query)
	
def getUrl(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    link = response.read()
    response.close()
    
    return link


def getDataVideo(url):

    link = getUrl(url)
   
    try:
    
        link = link.decode("ISO-8859-1")
        data =json.loads(link)
        
    except ValueError:
        return None
            
    except TypeError:
        return None
        
    except:
        return None
        
    else:
        if len(data) > 0:
        
            return data
            
        else:
            return None
            

  
base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

xbmcplugin.setContent(addon_handle, 'movies')

mode = args.get('mode', None)
url = args.get('url', [''])
name = args.get('name', None)
  


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)


    
    
if mode==None:
   
    index()
        
elif mode[0]=='destaquem':
  
    listDestaquem()
    
elif mode[0]=='noperdis':
   
    listNoPerdis()
    
elif mode[0]=='mesvist':

    listMesVist()

elif mode[0]=='programes':

    dirSections()    

elif mode[0]=='sections':

    listSections(url[0])  

elif mode[0]=='listvideos':
   
    listVideos(url[0])
    

elif mode[0]=='dirAZemisio':
   
    dirAZ_emisio()  

elif mode[0]=='dirAZtots':
   
    dirAZ_tots()       

elif mode[0]=='listAZemisio':
   
    listProgramesAZ(url_programes_emisio,url[0])
    
elif mode[0]=='listAZtots':
   
    listProgramesAZ(url_programes_tots, url[0])     
    
elif mode[0]=='directe':
   
    listDirecte()     
    
    

---
layout: post
title: Setup-and-home-media-server-using-docker
description: 
category: 
tags: 
---
{% include JB/setup %}

This article records the steps on how to setup home media servers using emby.

# About Emby 

[Emby](https://emby.media/about.html) provided servers/clients to share the medias across your different devices. Which is convient for home media sharing usage. The server can be running on x64/arm platforms.


# Server installation using docker
[Emby docker](https://hub.docker.com/r/emby/embyserver) tells how to setup emby sever using [docker](https://www.docker.com/get-started). The installation of docker itself  is beyond the scope of this article.

* Pull emby docker image
```bash
docker pull emby/embyserver:latest
```
*  Run emby server
```bash
docker run -d \
    --volume /path/to/programdata:/config \ # This is mandatory
    --volume /path/to/share1:/mnt/share1 \ # To mount a first share
    --volume /path/to/share2:/mnt/share2 \ # To mount a second share
    --device /dev/dri/renderD128 \ # To mount a render node for VAAPI
    --publish 8096:8096 \ # To expose the HTTP port
    --publish 8920:8920 \ # To expose the HTTPS port
    --env UID=`id -u`\ # The UID to run emby as (default: 2)
    --env GID=`id -g`\ # The GID to run emby as (default 2)
    --env GIDLIST=100 \ # A comma-separated list of additional GIDs to run emby as (default: 2)
    emby/embyserver:latest
```

1. You could replace the `/path/to/programdata` to a host path where you want to store the emby server meta data. Also you could optionally leave that alone, just store the data inside the container itself, but that's not encouraged, because you want the data to be persistented, while the filesystem of docker it self is a tempory filesystem.  Make it a persisted storage path outside the docker make it easy to copy/backup/share acorss different server instance, especially  if you want to migrate the server to some newer version docker image.

2. the `/path/to/share1/:/mnt/share1` could by any path pairs between host/container. `/path/to/share1` should be where you store all your medias/movie/photos/music on the host system. And you must provide this path to the container so it's visible to the emby server program inside the docker. Same as the `/path/to/share2`, and you could add any number of the paths as `--volume` paramters.

3. the two options `--publish 8096:8096` and `--publish 8920:8920`, the host port can be any port number, while the container port should be leave as it is. Because the emby server program inside the container make the asummption on these defaults port. To be more specific, you could replace the parameters as `--publish 8899:8096` and `--publish 10000:8920`

4. the two options `--env UID` and `--env GID` should be the uid/gid of the paths/files you want to share, this way the server program inside the docker can read/write the files preserving the consisten permission of host system.  Normally it's the uid/gid of the current user who execute the this docker command. 

5. the option `--GIDLIST` is not so clear to me. You can leave it as it is, or you need some more time to figure it out.

* Open the browser to config the server
Once your docker container started, you could type `http://localhost:8096` in the same system where you execute the command, through the website you could config the server interactively. It's very intutively, and no specicial tutortial/instuction is needed. You could also find the details on the emby website.

# Access the media server
You have serveral ways to access the media server after it successfully starts and configged.
Here is a list of supported platforms from [emby official website](https://emby.media/download.html).
The following ones are what I am using.
1.  Broweser, just access the `http://YOUR_IP:8096` through any browseer, the `YOUR_IP` is the ip address of your host sever which runs the emby docker container. It can be public IP address and also the local network adress, based on your configuration. Local address is always accessible, while the remote address (WLAN) can be turned off, if you don't want to expose your media server to external internet for security/privacy consideration.
2. Android client: Install emby from google store, or here is an [APK from official](https://github.com/MediaBrowser/Emby.Releases/raw/master/android/MediaBrowser.Mobile-googlearmv7-release.apk)
3. Android TV client: download the APK from the [apkmirror](https://www.apkmirror.com/?post_type=app_release&searchtype=apk&s=emby)

# Stop/Resume the server
* You could stop server by two ways
1. Stop the server by the client.
2. Stop the docker container in host system.
```bash
    #Suppose your docker container's name is "media_server", replace to anyname of yuor container's name
    docker stop media_server
```
* Resume the server
In the host system
```bash
    #Suppose your docker container's name is "media_server", replace to anyname of yuor container's name
    docker start media_server
```
import pydub, os, pafy, vlc


class NabiPlayer(Object):
	def __init__(self):
		self.MusicDir = "D:/Kuroihi_files/Google Drive/NabiBot/Plugins/YTMP_Songs/"
		self.playlists = []
		self.curPlaylist = self.playlists[0]
		self.instance = vlc.Instance()
		self.player = self.instance.media_player_new()
		self.repeating = False
	def getPlaylistsFromDir(self, dir):
		pass
	def updateProgressBar(self):
		pass
	def toggleRepeat(self, arg = None):
		self.repeating = not self.repeating
	def getSongName(self):
		return self.curPlaylist.getCurSong().getName()
	def getPlaylistDir(self):
		return self.curPlaylist.getDir()
	def pause(self, arg = None):
		self.player.pause()
	def play(self, arg = None):
		self.player.play()
	def repeat(self, arg = None):
		self.player.set_time(0)
		self.player.play()
	def isSongOver(self, arg = None):
		if self.player.get_length() - self.player.get_time() == 0:
			self.repeat()
		elif self.player.get_length() - self.player.get_time() < 1000:
			if self.repeating:
				self.repeat()
			else:
				self.next()			
	def next(self, arg = None):
		nextSong = self.curPlaylist.getNextSong()
		if nextSong != None:
			self.player.set_media(self.instance.media_new(nextSong))
		else:
			print("This is the last song in this playlist")
	def previous(self, arg = None):
		previousSong = self.curPlaylist.getPreviousSong()
		if previousSong != None:
			self.player.set_media(self.instance.media_new(previousSong))
		else:
			print("This is the first song in this playlist")
	def download(self, vidOrSong):
		self.curPlaylist.downloadToPlaylist(vidOrSong)
	def setPlaylist(self, playlistStr = None, playlistObj = None):
		if playlistStr != None:
			for PL in self.playlists:
				if PL.isEqualTo(playlistStr):
					self.curPlaylist = PL
					return None
			print("<NabiPlayer.setPlaylist> playlist doesn't appear to exist. If you want a new playlist, call NabiPlayer.addPlayList()")
		elif playlistObj != None:
			if playlistObj in self.playlists:
				self.curPlaylist = playlistObj
			else:
				self.curPlaylist = playlistObj
				self.playlists.append(playlistObj)
		else:
			print("<NabiPlayer.setPlaylist> recieved no input")
	
	def setSong(self, songStr = None, songObj = None):
		if songObj != None:
			song = songObj
		elif songStr != None:
			song = songStr
		else:
			print("<NabiPlayer.setSong> recieved no input")
			return None
		if self.curPlaylist.hasSong(song):
			self.curPlaylist.setCurSong(song)
		else:
			for PL in self.playlists:
				if PL.hasSong(song):
					self.curPlaylist = PL
					PL.setCurSong(song)
					return None
			print("<NabiPlayer.setSong> song doesn't appear to exist in any playlists ^_^;")
#







class Playlist(Object):
	def __init__(self, dir):
		temp = dir.split("/")
		self.name = temp[len(temp)-1]
		self.dir = dir
		# self.videos = getVideosFromDir(dir)
		self.songs = getSongsFromDir(dir)
		self.curSongIndex = 0
	
	def getSongsFromDir(self, dir):
		pass
	def getVideosFromDir(self, dir):
		pass
	def PafyWillWork(self, url):
		try:
			return pafy.new(url)
		except:
			print("Unknown Pafy Failure, retrying...")
			return self.PafyWillWork(url)
	def download(self, link, isVideo = False):
		if link.decode("utf-8-sig")[0:24] == u"https://www.youtube.com/":
			print("YOUTUBE URL: " + url)
			video = PafyWillWork(link.decode("utf-8-sig"))
			if isVideo:
				best = video.getbestvideo()
				title = best.title.replace(u"/", u"-").replace(u":", u";").replace(u"\"", u" ").replace(u"\\", u"-").replace(u"\'", u" ").replace(u"*", u"+").replace(u">", u"-").replace(u"<", u"-").replace(u"|", u"I").replace(u"?", u".")
				if not self.hasSong(title):
					print("<Playlist.download> ERROR: cannot download a video without the song being in the playlist")
					return False
				else:
					relatedSong = self.getSongByTitle(title)
			else:
				best = video.getbestaudio()
			title = best.title.replace(u"/", u"-").replace(u":", u";").replace(u"\"", u" ").replace(u"\\", u"-").replace(u"\'", u" ").replace(u"*", u"+").replace(u">", u"-").replace(u"<", u"-").replace(u"|", u"I").replace(u"?", u".")
			fileName = title + "." + best.extension
			for song in self.songs:
				songNameUN = unicode(song.getName(), "utf-8-sig")
				if songNameUN == fileName:
					return False
			newSongDir = self.dir + title + "." + best.extension
			if video.length > 600:
				print("Song is Longer than 10 min Owo, Nabi isn't downloading it -3-")
				return False
			else:
				print("Nabi is Downloading the song ^w^, Please wait...")
				best.download(filepath = newSongDir, quiet = False)
				print("")
				print("Done!")
				if isVideo:
					relatedSong.setVidDir(newSongDir)
				else:
					new = Song(fileName, newSongDir, link)
					self.songs.append(new)
				return True
		else:
			print("<Playlist.download> The link is not a youtube link in standard form")
	def isEqualTo(self, value):
		if type(value) == type(""):
			if value == self.name:
				return True
			else:
				return False
		print("<Playlist.isEqualTo> value is not of a handled type, defaulting False")
		return False
	def getSongByTitle(self, title):
		for song in self.songs:
			if song.getName(True) == title:
				return song
		return None
	def hasSong(self, value):
		if type(value) == type(""):
			for song in self.songs:
				if song.getName(True) == value:
					return True
		else:
			if value in self.songs:
				return True
		return False
	def getName(self):
		return self.name
	def getDir(self):
		return self.dir
	def getPreviousSong(self):
		if self.curSongIndex == 0: 
			return None
		else:
			self.curSongIndex -= 1
			return self.songs[self.curSongIndex]
	def getCurSong(self):
		return self.songs[self.curSongIndex]
	def getNextSong(self):
		if self.curSongIndex == len(self.songs) - 1: 
			return None
		else:
			self.curSongIndex += 1
			return self.songs[self.curSongIndex]
	def setCurSong(self, song):
		for i in range(len(self.songs)):
			if type(value) == type(""):
				if self.songs[i].getName() == value:
					self.curSongIndex = i
					return True
			else:
				if self.songs[i] == value:
					self.curSongIndex = i
					return True
		return False
	def isCurSong(self, song):
		if self.songs[self.curSongIndex] == song:
			return True
		elif self.songs[self.curSongIndex].getName() == song:
			return True
		elif self.songs[self.curSongIndex].getName(True) == song:
			return True
		return False
#






class Song(Object):
	def __init__(self, title, dir, link = None, vidDir = None):
		self.title = title
		self.dir = dir
		self.vidDir = vidDir
		self.link = link
	def getName(self, noExtension = False):
		if noExtension:
			temp = self.title.split(".")
			out = ".".join(temp[:-1])
			return out
		else:
			return self.title
	def getDir(self):
		return self.dir
	def getLink(self):
		return self.link
	def setLink(self, url):
		if url.decode("utf-8-sig")[0:24] == u"https://www.youtube.com/":
			self.link = url
		else:
			print("<Song.setLink> The link is not a youtube link in standard form")
	def getVidDir(self):
		return self.vidDir
	def setVidDir(self, vidDir):
		self.vidDir = vidDir


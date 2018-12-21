#coding: utf-8
import pydub
import os
import pafy
import vlc
instance = vlc.Instance()
instance2 = vlc.Instance()
def log(message):
	with open("GUI/Log.nabi", "a") as f:
		f.write(str(message)+"\n")
musicDir = "D:/Kuroihi_files/Google Drive/NabiBot/Plugins/YTMP_Songs/Music/"
# musicDir = "../../Plugins/YTMP_Songs/Music/"
previousSongsDir = "YTMPlayer/PreviousSongs.txt"
musicListDir = "YTMPlayer/MusicList.txt"
musicQueueDir = "YTMPlayer/MusicQueue.txt"
curSongDir = "YTMPlayer/CurSong.txt"
mode = "default"

player = instance.media_player_new()
vidPlayer = instance2.media_player_new()

def downloadVideo():
	with open(curSongDir, "r+") as f:
		for line in f:
			check = line.split("<VIDEOURL>")
			if len(check) == 2 and url.decode("utf-8-sig")[0:24] == u"https://www.youtube.com/":
				log("YOUTUBE URL: " + url)
				def repeatTrying():
					log("Unknown Pafy Failure, retrying...")
					try:
						return pafy.new(url)
					except:
						return repeatTrying()
				try:
					video = pafy.new(url.decode("utf-8-sig"))
				except:
					video = repeatTrying()
				bestVideo = video.getbestvideo()
				filePath = videoDir + check[0].split(".")[0] + bestVideo.extension
				log("Nabi is Downloading it ^w^, Please wait...")
				filename = bestVideo.download(filepath = filePath, quiet = False)
				log("")
				f.seek(0)
				fStart = len(check[0]) + len("<VIDEOURL>") + 1
				f.write(check[0] + "<VIDEOURL>" + filePath)
				f.truncate()
				vidPlayer.set_media(instance2.media_new(filePath))
				

def getAudioFromUrl(url = "", bestAudio = None):
	print url.split(".")[-1]
	if bestAudio != None:
		bestaudio = bestAudio
	elif url.split(".")[-1] == "mp3":
		with open(musicListDir, "r+") as f:
			for line in f:
				# print(type(line))
				lineUN = unicode(line.strip(), "utf-8-sig").split(".")[:-1]
				urlUN = unicode(url.strip(), "utf-8-sig").split(".")[:-1]
				if lineUN == urlUN:
					return musicDir.replace("/", "\\") + ".".join(lineUN) + ".mp3"
		return False
	elif url.decode("utf-8-sig")[0:24] == u"https://www.youtube.com/":
		log("YOUTUBE URL: " + url)
		def repeatTrying():
			log("Unknown Pafy Failure, retrying...")
			try:
				return pafy.new(url)
			except:
				return repeatTrying()
		try:
			video = pafy.new(url.decode("utf-8-sig"))
		except:
			video = repeatTrying()
		bestaudio = video.getbestaudio()
	else:
		log("invalid url:" + url)
		return False
	with open(musicListDir, "r+") as f:
		for line in f:
			lineUN = unicode(line.strip(), "utf-8-sig")
			title = bestaudio.title.replace(u"/", u"-").replace(u":", u";").replace(u"\"", u" ").replace(u"\\", u"-").replace(u"\'", u" ").replace(u"*", u"+").replace(u">", u"-").replace(u"<", u"-").replace(u"|", u"I").replace(u"?", u".")
			fileName = title + "." + bestaudio.extension
			if lineUN == fileName:
				return musicDir.replace("/", "\\") + lineUN
		filePath = musicDir + title + "." + bestaudio.extension
		if video.length > 600:
			log("Song is Longer than 10 min Owo, Nabi isn't downloading it -3-")
			return False
		else:
			log("Nabi is Downloading it ^w^, Please wait...")
			filename = bestaudio.download(filepath = filePath, quiet = False)
			log("")
		f.write(fileName.encode("utf-8") + "\n")
		f.truncate()
	return filename
		
def commandLine():
	userinput = raw_input("enter a url to get the audio: ")
	curMusic = getAudioFromUrl(url = userinput)
	os.startfile(curMusic)

def nextSongCheck():
	# print (player.get_length() - player.get_time())/1000.0
	if player.get_length() - player.get_time() == 0:
		playCurSong()
	elif player.get_length() - player.get_time() < 1000:
		if mode == "default":
			nextSong()
		elif mode == "repeat":
			playCurSong()

def nextSong(opt=None):
	with open(musicQueueDir,"r+") as f:
		d = f.readline()
		if len(d.strip()) > 0:
			curMusic = getAudioFromUrl(url = d.strip())
			if curMusic != False:
				curMusic = curMusic.replace("\\", "/")
				newFileName = ".".join(curMusic.split(".")[:-1])+".mp3"
				try:
					with open(newFileName) as test:
						log("Existing Song Found!")
				except:
					try:
						with open(curMusic, "rb") as song:
							song = pydub.AudioSegment.from_file(song, curMusic.split(".")[-1])
						log("Converting to mp3...")
						song.export(newFileName, "mp3")
						log("Deleting old file...")
						os.remove(curMusic)
						log("Done!")
					except:
						log("Neither file exists for:  " + newFileName + "  \\(XoX)/")
				media = player.get_media()
				if media != None:
					with open(previousSongsDir, "r+") as mQ:
						media.parse()
						mD = mQ.readlines()
						mD.insert(0, media.get_meta(0) + "\n")
						mQ.seek(0)
						for line in mD:
							if isinstance(line, str):
								line = line.decode("utf-8")
							mQ.write(line.encode("utf-8"))
				player.set_media(instance.media_new(newFileName))
				player.play()
		first = True
		f.seek(0)
		d = f.readlines()
		f.seek(0)
		for line in d:
			if first:
				first = False
				continue
			else:
				f.write(line)
		f.truncate()
	updateCurSong()

def prevSong(opt=None):
	with open(previousSongsDir, "r+") as f:
		d = f.readlines()
		f.seek(0)
		dS = f.readline().strip().decode("utf-8-sig")
		if len(dS) > 0:
			media = player.get_media()
			if media != None:
				with open(musicQueueDir, "r+") as mQ:
					media.parse()
					mD = mQ.readlines()
					mD.insert(0, media.get_meta(0) + "\n")
					mQ.seek(0)
					for line in mD:
						if isinstance(line, str):
							line = line.decode("utf-8")
						mQ.write(line.encode("utf-8"))
			curSong = getAudioFromUrl(url = d[0].strip())
			if curSong != False:
				curSong = curSong.replace("\\", "/")
				try:
					with open(curSong) as test:
						log("Existing Song Found!")
				except:
					log("WTF JUST HAPPENED!?!")
				f.seek(0)
				first = True
				for line in d:
					if first:
						first = False
						continue
					else:
						f.write(line)
				f.truncate()
				player.set_media(instance.media_new(curSong))
				player.play()
	updateCurSong()

def playCurSong(arg = None):
	with open(curSongDir, "r") as f:
		d = f.readline().strip()
		curSong = getAudioFromUrl(url = d)
		if curSong != False:
			curSong = curSong.replace("\\", "/")
			try:
				with open(curSong) as test:
					log("Existing Song Found!")
			except:
				log("WTF JUST HAPPENED!?!")
			player.set_media(instance.media_new(curSong))
			player.play()
		else:
			nextSong()
		
def getCurSong():
	media = player.get_media()
	if media != None:
		media.parse()
		return media.get_meta(0)
	else:
		return ""

def updateCurSong():
	with open(curSongDir, "w") as f:
		f.write(getCurSong().encode("utf-8"))
		f.truncate()

def toggleMode(arg = None, returnOnly = False):
	global mode
	if returnOnly:
		if mode == "default":
			return "default"
		elif mode == "repeat":
			return "#000033"
		else:
			print "mode change error in toggleMode returnOnly"
			return "default"
	else:
		print("toggling")
		if mode == "default":
			mode = "repeat"
		elif mode == "repeat":
			mode = "default"
		else:
			mode = "default"
			print "mode change error in toggleMode"
def progressBarUpdate():
	length = 47.5
	timePerChar = float(player.get_length()) / length
	numOfChars = float(player.get_time()) / timePerChar
	charString = ""
	for i in range(int(numOfChars)):
		charString += "█"
	if numOfChars - int(numOfChars) < 0.125: pass
	elif numOfChars - int(numOfChars) < 0.250: charString += "▏"
	elif numOfChars - int(numOfChars) < 0.375: charString += "▎"
	elif numOfChars - int(numOfChars) < 0.500: charString += "▍"
	elif numOfChars - int(numOfChars) < 0.625: charString += "▌"
	elif numOfChars - int(numOfChars) < 0.750: charString += "▋"
	elif numOfChars - int(numOfChars) < 0.875: charString += "▊"
	else: charString += "▉"
	return charString

def playVideo():
	vidPlayer.play()
	
def closeVideo():
	vidPlayer.release()

def setHandle(videoFrame):
	vidPlayer.set_hwnd(videoFrame.winfo_id())
	
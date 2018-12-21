with open("KaomojiAll.nabi", "rb") as f:
	Kaomoji = "".decode("utf-8", "replace").encode("utf-8", "replace")
	for line in f:
		text = line.strip()
		Kaomoji += text.decode("utf-8", "replace").encode("utf-8", "replace")
	Kmoji = eval(Kaomoji)
raw_input("Number of Kaomoji loaded: " + str(len(Kmoji)))
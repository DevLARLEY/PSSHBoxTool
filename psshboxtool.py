import sys, re
import base64
from itertools import zip_longest
import xml.etree.ElementTree as et

class c:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class p:
	INFO = '[' + c.GREEN + 'INFO' + c.ENDC + '] '
	WARN = '[' + c.YELLOW + 'WARN' + c.ENDC + '] '
	ERROR = '[' + c.RED + 'EROR' + c.ENDC + '] '

class sysid:
	widevine = 'edef8ba979d64acea3c827dcd51d21ed'
	playready = '9a04f07998404286ab92e65be0885f95'
	fairplay = '94ce86fb07ff4f43adb893d2fa968ca2'
	common = '1077efecc0b24d02ace33c1e52e2fb4b'
	fiarplay2 = '29701fe43cc74a348c5bae90c7439a47'

psshheader = '70737368'
bar = '╔═════════════╣ '
bar3 = '══════════════╣ '
bar2 = ' ╠══════════════'
data = ''

def printLogo():
	print()
	print(c.GREEN + "       ______  ______ ____ __   __ " + c.RED + "_____         " + c.YELLOW + "________         __  ")
	print(c.GREEN + "      /_____/\\/_____//____/_/| /_/" + c.RED + "/____/\\       " + c.YELLOW + "/_______/|       /_/|")
	print(c.GREEN + "      |  __ \\ / ____/ ____| ||_| |" + c.RED + "|  _ \\/|___ __" + c.YELLOW + "|__   __|/_  ____| ||")
	print(c.GREEN + "      | |/_) | (___/ (___/| |/_| |" + c.RED + "| |_) |/___/_//_/" + c.YELLOW + "| ||___/\\/___/| ||")
	print(c.GREEN + "      |  ___/ \\___ \\\\___ \\|  __  |" + c.RED + "|  _ < / _ \\ \\/ /" + c.YELLOW + "| |/ _ \\// _ \\| ||")
	print(c.GREEN + "      | ||   /____) |___) | || | |" + c.RED + "| |_) | (_) >  < " + c.YELLOW + "| | (_) | (_) | ||")
	print(c.GREEN + "      |_|/   |_____/_____/|_|/ |_|" + c.RED + "|____//\\___/_/\\_\\" + c.YELLOW + "|_|\\___/ \\___/|_|/" + c.ENDC)
	print("                    (c) https://github.com/DevLARLEY")
	print()

def rev(s):
    return ''.join(str(x) for x in list(reversed([i+j for i,j in zip_longest(s[::2], s[1::2], fillvalue='0')])))

def appZero(s):
	return ''.join(str(x) for x in [ss + '00' for ss in list([i+j for i,j in zip_longest(s[::2], s[1::2], fillvalue='0')])])

def ss(str, s, e):
	return str[s:e]

def conv(s):
	return bytes.fromhex(s.replace("00", "")).decode('utf-8')

def fi(h, flip=False):
	if flip:
		return str(int(rev(h), 16))
	else:
		return str(int(h, 16))

def fs(h, flip=False):
	if flip:
		return bytes.fromhex(rev(h)).decode('utf-8')
	else:
		return bytes.fromhex(h).decode('utf-8')

def split(strng, sep, pos):
    strng = strng.split(sep)
    return sep.join(strng[:pos]), sep.join(strng[pos:])

def chooseMode():
	i = input(p.INFO + "Choose Mode => (1) Dump PSSH, (2) Create PSSH, (3) Split PSSH ~: ")
	if i != '1' and i != '2' and i != '3':
		print(p.ERROR + 'No option was chosen.')
		sys.exit()
	else:
		return int(i)

def getFullBoxVersion(h):
	return int(ss(h, 16, 18), 16)

def getPSSHType(pssh):
	typ = []
	h = base64.b64decode(pssh).hex().upper()
	if sysid.widevine in h:
		typ.append('1')
	if sysid.playready in h:
		typ.append('2')
	if sysid.fairplay in h:
		typ.append('3')
	if sysid.common in h:
		typ.append('4')
	if sysid.fiarplay2 in h:
		typ.append('5')
	return typ

#TODO maybe change this to find pssh header
def searchForSysID(h):
	search = [sysid.widevine, sysid.playready, sysid.fairplay, sysid.common, sysid.fiarplay2]
	f = []
	for s in search:
		f.extend([m.start() for m in re.finditer(s, h)])
	f.sort()
	f = [*map(lambda x: x-24, f)]
	return f

def formatOutput():
	string = input(p.INFO + "Format output (y/n)? ~: ")
	if string.lower() == 'y':
		return True
	else:
		return False

def fill(f, u):
	return ('0'*(u-len(f)) + f)

def chooseSystemID():
	print(p.INFO + "Select System ID:")
	print(p.INFO + "(1) " + sysid.widevine + " (Widevine)")
	print(p.INFO + "(2) " + sysid.playready + " (PlayReady)")
	print(p.INFO + "(3) " + sysid.fairplay + " (FairPlay)")
	print(p.INFO + "(4) " + sysid.common + " (Common)")
	print(p.INFO + "(5) " + sysid.fiarplay2 + " (Netflix Fairplay)")
	s = input(p.INFO + "~: ")
	if s == '1':
		return sysid.widevine
	elif s == '2':
		return sysid.playready
	elif s == '3':
		return sysid.fairplay
	elif s == '4':
		return sysid.common
	elif s == '5':
		return sysid.fiarplay2
	else:
		print(p.ERROR + "No option was chosen.")
		sys.exit()

def isZeroed(s):
	if len(s) % 2 != 0:
		return False
	ar = [i+j for i,j in zip_longest(s[::2], s[1::2], fillvalue='0')]
	for a in range(len(ar)):
		if a % 2 != 0:
			if ar[a] != '00':
				return False
	return True

def isHex(s):
	try:
		int(s, 16)
	except Exception:
		return False
	return True

def queryAdditionalFields():
	ad = input(p.INFO + "Add additional Fields (y/n)? ~: ")
	if ad.lower() == 'y':
		return True
	return False

def conv08(s):
	if s == 'False':
		return '00'
	elif s == 'True':
		return '01'

def conv48(s):
	if s == 'cenc':
		return 'e3dc959b06'
	elif s == 'cbc1':
		return 'b1c6899b06'
	elif s == 'cens':
		return 'f3dc959b06'
	elif s == 'cbcs':
		return 'f3c6899b06'

def addAdditionalFields(fields):
	print(p.INFO + "Select field to add:")
	print(p.INFO + "(08) Alogrithm (False -> Not encrypted, True -> AES-CTR)")
	print(p.INFO + "(12) Key ID (any)")
	print(p.INFO + "(1a) Provider (any)")
	print(p.INFO + "(22) Content ID (any)")
	print(p.INFO + "(2a) Track Type (any)")
	print(p.INFO + "(32) Policy (any)")
	print(p.INFO + "(48) Protection Scheme (cenc, cbc1, cens, cbcs)")
	i = input(p.INFO + "~: ")
	a = ['08', '12', '1a', '22', '2a', '32', '48']
	lo = i.lower()
	if lo in a:
		val = input(p.INFO + cWVT(lo) + " Value ~: ")
		if lo == '08':
			a = ['true', 'false']
			if val.lower() in a:
				fields += lo
				fields += conv08(val)
			else:
				print(p.ERROR + "Incorrect value input.")
				sys.exit()
		elif lo == '48':
			a = ['cenc', 'cbc1', 'cens', 'cbcs']
			if val.lower() in a:
				fields += lo
				fields += conv48(val)
			else:
				print(p.ERROR + "Incorrect value input.")
				sys.exit()
		elif lo == '12':
			fields += lo
			val = val.replace('-', '')
			if isHex(val):
				h = val
			else:
				print(p.ERROR + "Incorrect value input (Input not hex).")
				sys.exit()
			fields += fill(decToHex(int(len(h))//2), 2)
			fields += h
		else:
			fields += lo
			if isHex(val):
				if not isZeroed(val):
					#h = appZero(val) #only on PlayReady
					h = val
				else:
					h = val
			else:
				#h = appZero(val.encode('utf-8').hex())
				h = val.encode('utf-8').hex()
			fields += fill(decToHex(int(len(h))//2), 2)
			fields += h
		if queryAdditionalFields():
			fields = addAdditionalFields(fields)
		else:
			global data
			data = fields
	else:
		print(p.ERROR + "No option was chosen.")
		ch = queryAdditionalFields()
		if ch:
			addAdditionalFields(fields)
		else:
			data = fields

def decToHex(dec):
	h = str(hex(dec))
	return ss(h, 2, len(h))

def constructPSSH(fullbox='0'*8, systemid='0'*32, fields=''):
	totalsize = '0'*8
	datasize = '0'*8
	o = (totalsize + psshheader + fullbox + systemid + datasize + fields)
	totalsize = fill(decToHex(int(len(o))//2), 8)
	datasize = fill(decToHex(int(len(fields))//2), 8)
	o = (totalsize + psshheader + fullbox + systemid + datasize + fields)
	return o

# --------- PlayReady --------- #

def xmlformat(xml):
	el = et.XML(xml)
	et.indent(el)
	out = et.tostring(el, encoding='unicode').replace("ns0:", "").replace(":ns0", "").split("\n")
	ret = []
	for o in range(len(out)):
		pr = out[o]
		if o == len(out)-1:
			ret.append("╚ " + pr)
		elif o == 0:
			ret.append("╠  " + pr)
		else:
			ret.append("║ " + pr)
	return ret

def convertPRType(t):
	if t == '1':
		return 'PlayReady Header Record'
	elif t == '2':
		return 'Reserved Record'
	elif t == '3':
		return 'Embedded License Store Record'
	else:
		return None

def formatPlayReady(info):
	data = info[0]
	print(p.INFO + "╠═╦═ " + c.BOLD + "Box:" + c.ENDC)
	print(p.INFO + "║ ╠ Total Size: " + fi(data[0]) + " bytes (" + data[0] + ")")
	print(p.INFO + "║ ╚ Type: " + fs(data[1]) + " (" + data[1] + ")")
	print(p.INFO + "╠═╦═ " + c.BOLD + "FullBox:" + c.ENDC)
	print(p.INFO + "║ ╠ Version: " + fi(ss(data[2], 0, 2)) + " (" + ss(data[2], 0, 2) + ")")
	print(p.INFO + "║ ╚ Flags: " + ss(data[2], 2, 8))
	print(p.INFO + "╚═╦═ " + c.BOLD + "PSSH Box:" + c.ENDC)
	print(p.INFO + "  ╠ System ID: " + data[3])
	print(p.INFO + "  ╠ Box Size: " + fi(data[4]) + " bytes (" + data[4] + ")")
	print(p.INFO + "  ╚═╦═ " + c.BOLD + "PlayReady Object:" + c.ENDC)
	print(p.INFO + "    ╠ Data Length: " + fi(data[5], True) + " bytes (" + data[5] + ")")
	print(p.INFO + "    ╠ Record Count: " + fi(data[6], True) + " (" + data[6] + ")")
	print(p.INFO + "    ╚═╦═ " + c.BOLD + "Records:" + c.ENDC)
	if len(info) > 1:
		recs = info[1]
		for r in range(len(recs)):
			rec = recs[r]
			if r != len(recs)-1:
				print(p.INFO + "      ╠═╦═ Record " + str(r+1) + ":")
				print(p.INFO + "      ║ ╠═ Type: " + convertPRType(fi(rec[0], True)) + " (" + rec[0] + ")")
				print(p.INFO + "      ║ ╠═ Length: " + fi(rec[1], True) + " bytes (" + rec[1] + ")")
				if fi(rec[0], True) == '1':
					print(p.INFO + "      ║ ╚═╦═ " + c.BOLD + "Value:" + c.ENDC)
					for q in xmlformat(rec[2]):
						print(p.INFO + "      ║   " + q)
				else:
					print(p.INFO + "      ║ ╚═══ Value: " + rec[2])
			else:
				print(p.INFO + "      ╚═╦═ Record " + str(r+1) + ":")
				print(p.INFO + "        ╠═ Type: " + convertPRType(fi(rec[0], True)) + " (" + rec[0] + ")")
				print(p.INFO + "        ╠═ Length: " + fi(rec[1], True) + " bytes (" + rec[1] + ")")
				if fi(rec[0], True) == '1':
					print(p.INFO + "        ╚═╦═ " + c.BOLD + "Value:" + c.ENDC)
					for q in xmlformat(rec[2]):
						print(p.INFO + "          " + q)
				else:
					print(p.INFO + "        ╚═══ Value: " + rec[2])
	print()

def getPlayReadyRecord(h, i):
	base = ss(h, 64, len(h))
	r = int(rev(ss(base, 8, 12)), 16)
	if i >= 1:
		if i <= r:
			c = 12
			for s in range(i-1):
				c += 4
				p = int(rev(ss(base, c, c+4)), 16)*2
				c += 4
				c += p
				l = p
			l = int(rev(ss(base, c+4, c+8)), 16)*2
			return ss(base, c, l+c+8)
		else:
			return None
	else:
		return None

def dumpPlayReadyPSSH(h):
	data = []
	byte = ss(h, 0, 84)

	#Data always present
	pos = [8, 8, 8, 32, 8, 8, 4]
	for p in range(len(pos)):
		start = 0
		for i in range(p):
			start += pos[i]
		data.append(ss(byte, start, pos[p]+start))

	#Variable Data
	headers = []
	for i in range(1, int(rev(ss(byte, 72, 76)), 16)+1):
		re = getPlayReadyRecord(h, i)
		value = ss(re, 8, len(re))
		typ = fi(ss(re, 0, 4), True)
		if typ == '1':
			value = conv(value)
		header = [ss(re, 0, 4), ss(re, 4, 8), value]
		headers.append(header)

	return [data, headers]

# --------- Widevine --------- #

def cWVT(typ):
	if typ == '08':
		return 'Algorithm'
	elif typ == '12':
		return 'Key ID (KID)'
	elif typ == '1a':
		return 'Provider'
	elif typ == '22':
		return 'Content ID'
	elif typ == '2a':
		return 'Track Type'
	elif typ == '32':
		return 'Policy'
	elif typ == '48':
		return 'Protection Scheme'

def cVal(ide, val):
	ids = ['1a', '2a', '32']
	if ide in ids:
		return fs(val)
	elif ide == '08':
		if val == '00':
			return 'no encryption'
		elif val == '01':
			return 'AES-CTR (cenc, full sample encryption)'
		else:
			return val
	elif ide == '48':
		if val == 'e3dc959b06':
			return 'cenc (AES-CTR full sample encryption)'
		elif val == 'b1c6899b06':
			return 'cbc1 (AES-CBC full sample encryption)'
		elif val == 'f3dc959b06':
			return 'cens (AES-CTR pattern encryption)'
		elif val == 'f3c6899b06':
			return 'cbcs (AES-CBC pattern encryption)'
		else:
			return val
	else:
		return val

def formatWidevine(info):
	data = info[0]
	print(p.INFO + "╠═╦═ " + c.BOLD + "Box:" + c.ENDC)
	print(p.INFO + "║ ╠ Total Size: " + fi(data[0]) + " bytes (" + data[0] + ")")
	print(p.INFO + "║ ╚ Type: " + fs(data[1]) + " (" + data[1] + ")")
	print(p.INFO + "╠═╦═ " + c.BOLD + "FullBox:" + c.ENDC)
	print(p.INFO + "║ ╠ Version: " + fi(ss(data[2], 0, 2)) + " (" + ss(data[2], 0, 2) + ")")
	print(p.INFO + "║ ╚ Flags: " + ss(data[2], 2, 8))
	print(p.INFO + "╚═╦═ " + c.BOLD + "PSSH Box:" + c.ENDC)
	print(p.INFO + "  ╠ System ID: " + data[3])
	print(p.INFO + "  ╠ Data: " + fi(data[4]) + " bytes (" + data[4] + ")")
	print(p.INFO + "  ╚═╦═ " + c.BOLD + "Widevine PSSH Data:" + c.ENDC)
	if len(info) > 1:
		recs = info[1]
		for r in range(len(recs)):
			rec = recs[r]
			if r == len(recs)-1:
				print(p.INFO + "    ╚═╦═ " + c.BOLD + cWVT(rec[0]) + c.ENDC)
				print(p.INFO + "      ╚ Value: " + cVal(rec[0], rec[1]))
			else:
				print(p.INFO + "    ╠═╦═ " + c.BOLD + cWVT(rec[0]) + c.ENDC)
				print(p.INFO + "    ║ ╚ Value: " + cVal(rec[0], rec[1]))
		
def extrPSSH(h, i):
	s = ss(h, i, len(h))
	spl = split(s, psshheader, 2)
	s = spl[0]
	if spl[1] != '':
		s = ss(s, 0, len(s)-8)
	return s

def extractBytes(h):
	d = []
	h = ss(h, 64, len(h))
	
	algo = ss(h, 0, 4)
	if algo == '0800':
		d.append(['08', '00'])
	elif algo == '0801':
		d.append(['08', '01'])

	search = ["12", "1a", "22", "2a", "32"]
	spl = [i+j for i,j in zip_longest(h[::2], h[1::2], fillvalue='0')]
	c = 0
	if algo == '0800' or algo == '0801':
		c = 4
	while True:
		s = ss(h, c, c+2)
		if len(s) < 2:
			break
		if s in search:
			c += 2
			l = int(ss(h, c, c+2), 16)*2
			d.append([s, ss(h, c+2, c+2+l)])
			c += l
			c += 2
		else:
			c += 2

	pas = ["48e3dc959b06", "48b1c6899b06", "48f3dc959b06", "48f3c6899b06"]
	for p in pas:
		if h.endswith(p):
			d.append(['48', ss(p, 2, len(p))]) #Crypto Period Index could come behind and make this useless => Develop a better alternative
	return d

def dumpWidevinePSSH(h):
	data = []
	byte = ss(h, 0, 64)

	#Data always present
	pos = [8, 8, 8, 32, 8]
	for p in range(len(pos)):
		start = 0
		for i in range(p):
			start += pos[i]
		data.append(ss(byte, start, pos[p]+start))

	#Variable Data
	var = extractBytes(h)

	return [data, var]

# --------- Main --------- #

def main():
	printLogo()

	mode = chooseMode()
	# Options:
	#  Dump PSSH
	#  Create PSSH (System ID, Key ID)
	#  Shrink PSSH

	#test if pssh header is even a pssh
	if mode == 1:
		pssh = input(p.INFO + "Input PSSH (Base64) ~: ")
		if pssh == '':
			print(p.ERROR + "No PSSH was entered.")
			sys.exit()

		try:
			h = base64.b64decode(pssh).hex()
		except Exception:
			print(p.ERROR + "Could not decode Base64 input.")
			sys.exit()

		ver = getFullBoxVersion(h)
		if ver == 0:

			f = searchForSysID(h)
			form = formatOutput()

			if len(f) > 0:
				print("\n" + p.INFO + "Detected " + str(len(f)) + " PSSH Strings(s):\n")

				for find in f:
					syst = ss(h, find+24, find+32+24)
					s = extrPSSH(h, find)

					if syst == sysid.widevine:
						print(p.INFO + "Google Widevine PSSH detected.")
						dump = dumpWidevinePSSH(s)
						if dump:
							if form:
								print(p.INFO + bar + c.BOLD + "Google Widevine PSSH Dump" + c.ENDC + bar2)
								formatWidevine(dump)
							else:
								print(p.INFO + bar3 + c.BOLD + "Google Widevine PSSH Dump" + c.ENDC + bar2)
								print(dump)
						else:
							print(p.ERROR + "No information found.")
					if syst == sysid.playready:
						print(p.INFO + "Microsoft PlayReady PSSH detected.")
						dump = dumpPlayReadyPSSH(s)
						if dump:
							if form:
								print(p.INFO + bar + c.BOLD + "Microsoft PlayReady PSSH Dump" + c.ENDC + bar2)
								formatPlayReady(dump)
							else:
								print(p.INFO + bar3 + c.BOLD + "Microsoft PlayReady PSSH Dump" + c.ENDC + bar2)
								print(dump)
						else:
							print(p.ERROR + "No information found.")
					if syst == sysid.fairplay:
						print(p.INFO + "Apple Fairplay PSSH detected.")
						print(p.ERROR + "Apple Fairplay PSSH is not supported.")
					if syst == sysid.common:
						print(p.INFO + "W3C Common PSSH detected.")
						print(p.ERROR + "W3C Common PSSH is not supported.")
					if syst == sysid.fiarplay2:
						print(p.INFO + "Netflix FairPlay PSSH detected.")
						print(p.ERROR + "Netflix FairPlay PSSH is not supported.")
			else:
				print(p.ERROR + "No PSSH found.")
		else:
			print(p.ERROR + "Fullbox Version " + str(ver) + " is not supported.")
	elif mode == 2:
		# Create PSSH
		print(p.WARN + "USING GENERATED PSSH STRINGS ON SITES THAT UTILIZE CUSTOM FORMATS COULD GET YOUR CDM BANNED!")
		systemid = chooseSystemID()
		fields = ''
		if queryAdditionalFields():
			addAdditionalFields(fields)
		o = constructPSSH('00000000', systemid, data)
		print(p.INFO + "Base16 => " + o)
		print(p.INFO + "Base64 => " + base64.b64encode(bytes.fromhex(o)).decode())
	elif mode == 3:
		#Split PSSH
		pssh = input(p.INFO + "Input PSSH (Base64) ~: ")
		if pssh == '':
			print(p.ERROR + "No PSSH was entered.")
			sys.exit()

		try:
			h = base64.b64decode(pssh).hex()
		except Exception:
			print(p.ERROR + "Could not decode Base64 input.")
			sys.exit()

		find = searchForSysID(h)
		l = len(find)
		if l < 2:
			print(p.ERROR + "Nothing to split. Only found " + str(l) + " PSSH String(s).")
			sys.exit()

		print("\n" + p.INFO + "Detected " + str(l) + " PSSH Strings(s):")
		for f in find:
			ps = extrPSSH(h, f)
			enc = base64.b64encode(bytes.fromhex(ps)).decode()
			syst = ss(h, f+24, f+32+24)

			print()
			if syst == sysid.widevine:
				print(p.INFO + "Google Widevine PSSH detected.")
				print(p.INFO + bar3 + c.BOLD + "Google Widevine PSSH Dump" + c.ENDC + bar2)
			elif syst == sysid.playready:
				print(p.INFO + "Microsoft PlayReady PSSH detected.")
				print(p.INFO + bar3 + c.BOLD + "Microsoft PlayReady PSSH Dump" + c.ENDC + bar2)
			elif syst == sysid.fairplay:
				print(p.INFO + "Apple Fairplay PSSH detected.")
				print(p.INFO + bar3 + c.BOLD + "Apple Widevine PSSH Dump" + c.ENDC + bar2)
			elif syst == sysid.common:
				print(p.INFO + "W3C Common PSSH detected.")
				print(p.INFO + bar3 + c.BOLD + "W3C Widevine PSSH Dump" + c.ENDC + bar2)
			elif syst == sysid.fiarplay2:
				print(p.INFO + "Netflix FairPlay PSSH detected.")
				print(p.INFO + bar3 + c.BOLD + "Netflix Widevine PSSH Dump" + c.ENDC + bar2)
			print(p.INFO + enc)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		sys.exit()
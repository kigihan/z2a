#!/usr/bin/python3
#coding=utf-8

import os
from os import listdir
from os.path import isfile, join
#本來拿來decod eunicode的(\u000d\u000a)，但是解出來會變成兩次換行，放棄，直接用replace做掉
#不過還是要用來解ZAP的hex格式body
import codecs

def txt_proc(filename):
	#讀檔
	file = open(filename, "r")
	#debug現在parse到哪個檔名
	#print("    [x] filename is : " + filename)
	#逐行讀取
	logresult = []
	logresult.append([])
	for line in file:
		#print("            [.] start FOR ")
		#print("            [.] FOR content: " + line)
		#找開頭是 "INSERT INTO HISTORY VALUES(" 的
		if "INSERT INTO HISTORY VALUES(" in line:
			#debug搜尋功能
			#print("            [*] I got the line: " + line)
			#call parse來切字串
			lineresult = parse(line)
			#debug切好的結果
			#print("            [X] Line Result Here: " + str(lineresult))
			#塞進同一個array
			logresult.append(lineresult)
			#debug全部內容的array
			#print("            [O] Log Result Is: " + str(logresult))
	#因為亂搞，logresult[0]是空的，把他砍掉先
	del logresult[0]
	return logresult

def parse(linetext):
	#掐頭去尾
	linetext_tmp = linetext[25:-2].split("(",1)
	cut_str = linetext_tmp[1]
	#前幾個用逗號切就可以了
	#print("            [*] cut it off: " + cut_str)
	split_str = cut_str.split(",",6)

	#開始出現大的字串，前後有單引號包夾，裡面包含逗號，懶得思考，用單引號慢慢切，低能苦工
	split_tmp_arr = split_str[6].split("\'",14)
	split_str6 = split_tmp_arr[1]
	split_str7 = split_tmp_arr[3]
	split_str8 = split_tmp_arr[5]
	split_str9 = split_tmp_arr[7]
	split_str10 = split_tmp_arr[9]
	split_str11 = split_tmp_arr[11]
	split_str12 = split_tmp_arr[12].replace(",","")
	split_str13 = split_tmp_arr[13]
	split_str14 = split_tmp_arr[14].replace(",","")
	"""
	split_tmp_arr = split_str[6].split("\'",12)
	split_str6 = split_tmp_arr[1]
	split_str7 = split_tmp_arr[3]
	split_str8 = split_tmp_arr[5]
	split_str9 = split_tmp_arr[7]
	split_str10 = split_tmp_arr[9]
	split_str11 = split_tmp_arr[11]
	split_str_tmp = split_tmp_arr[12]

	#穿插一個沒有單引號的，改回逗號
	split_tmp_arr = split_str_tmp.split(",",2)
	split_str12 = split_tmp_arr[1]
	split_str_tmp = split_tmp_arr[2]
	#單引號
	split_tmp_arr = split_str_tmp.split("\'",2)
	split_str13 = split_tmp_arr[1]
	split_str_tmp = split_tmp_arr[2]
	#又穿插一個沒有單引號的，改回逗號
	split_tmp_arr = split_str_tmp.split(",",2)
	split_str14 = split_tmp_arr[1]
	"""

	#parse完整行字串了，開始把資料塞回split_str
	split_str[6] = split_str6
	#因為一開始只切成7份(0~6)，後面的塞不下，用append擴展
	split_str.append(split_str7)
	split_str.append(split_str8)
	split_str.append(split_str9)
	split_str.append(split_str10)
	split_str.append(split_str11)
	split_str.append(split_str12)
	split_str.append(split_str13)
	split_str.append(split_str14)

	#拆AppScan要的欄位出來
	#從str7拆http, host, path, port出來用
	split_str_tmp = split_str7
	split_tmp_arr = split_str_tmp.split("://",1)
	#str7是HTTP/HTTPS
	split_str7 = split_tmp_arr[0]
	split_str_tmp = split_tmp_arr[1]

	split_tmp_arr = split_str_tmp.split("/",1)

	#str8是host
	split_str8 = split_tmp_arr[0]
	#str9是path
	if len(split_tmp_arr) == 2:
		#split_str9 = "/" + split_tmp_arr[1]
		if "?" in split_tmp_arr[1]:
			#print("IGOTIT")
			split_str_tmp = split_tmp_arr[1]
			split_tmp_arr = split_str_tmp.split("?", 1)
			split_str9 = "/" + split_tmp_arr[0]
		else:
			split_str9 = "/" + split_tmp_arr[1]
	elif len(split_tmp_arr) == 1:
		split_str9 = "/"

	#split_str10是port
	if split_str7.lower() == "http":
		split_str10 = "80"
	elif split_str7.lower() == "https":
		split_str10 = "443"

	split_str.append(split_str7)
	split_str.append(split_str8)
	split_str.append(split_str9)
	split_str.append(split_str10)

	#debug新parse好的array結果
	"""
	print("                [o] log[0] is: " + split_str[0] +
		   "\n                [o] log[1] is: " + split_str[1] +
		   "\n                [o] log[2] is: " + split_str[2] +
		   "\n                [o] log[3] is: " + split_str[3] +
		   "\n                [o] log[4] is: " + split_str[4] +
		   "\n                [o] log[5] is: " + split_str[5] +
		   "\n                [o] log[6] is: " + split_str[6] +
		   "\n                [o] log[7] is: " + split_str[7] +
		   "\n                [o] log[8] is: " + split_str[8] +
		   "\n                [o] log[9] is: " + split_str[9] +
		   "\n                [o] log[10] is: " + split_str[10] +
		   "\n                [o] log[11] is: " + split_str[11] +
		   "\n                [o] log[12] is: " + split_str[12] +
		   "\n                [o] log[13] is: " + split_str[13] +
		   "\n                [o] log[14] is: " + split_str[14])
	"""

	return split_str

#切曲奇囉
def cookie_knife(cookies):
	#先用\u000d\u000a的換行符號切
	cookie_sliced = cookies.split("\u000d\u000a")
	#把第一行的GET XXX拿掉，最後因為有兩次換行，會切出兩個空值，也拿掉
	cookie_sliced = cookie_sliced[1:-2]
	cookie_packaged = {}
	#找到Cookie: 那行
	for field in cookie_sliced:
		if field.lower().startswith("cookie: "):
			#把前面的Cookie: 去掉，塞進cookie_box
			cookie_box = field[8:]
	try:
		#現在剩cookie了，用分號切
		cookie_box = cookie_box.split("; ")
		#再用=切出key跟value，塞進cookie_packaged
		for field in cookie_box:
			key,value = field.split("=")
			cookie_packaged[key] = value
		#debug 切出來的結果
		#print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
		#print(cookie_packaged["SERVERID"])
		#for a in cookie_packaged:
		#	print(a + " : " + cookie_packaged[a])
		#print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n")
	except:
		cookie_packaged = ""

	#把切好的cookie丟回去
	return cookie_packaged

#打包cookie成AppScan格式
def cookie_wrap_up(path, domain, cookie_bag):
	cookie_content = ""
	"""
	把各個cookie都抓出來拼；cookie name是key，cookie value是cookie_bag[key]
	secure跟expires暫時不想處理，塞固定值先，有問題再說
	"""
	for key in cookie_bag:
		cookie_content += "    <cookie name=\"" + key + "\" value=\""
		if cookie_bag[key] == "\"\"":
			cookie_bag[key] = ""
		cookie_content += cookie_bag[key] + "\"" \
		               + " path=\"" + path + "\" domain=\"" + domain + "\"" \
					   + " secure=\"False\" expires=\"01/01/0001 00:00:00\" />\n"
	#print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
	#print(cookie_content)
	#print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n")
	return cookie_content

#組合輸出內容
def compose(material):
	#print("\ngggggggggggggggggg\n" + str(material) + "\n" + str(len(material)))
	newcontent = ""
	for n in range(len(material)):
		"""
		newcontent += "                [o] log[0] is: " + material[n][0] + \
			   		  "\n                [o] log[1] is: " + material[n][1] + \
			   		  "\n                [o] log[2] is: " + material[n][2] + \
			   		  "\n                [o] log[3] is: " + material[n][3] + \
			   		  "\n                [o] log[4] is: " + material[n][4] + \
			   		  "\n                [o] log[5] is: " + material[n][5] + \
			   		  "\n                [o] log[6] is: " + material[n][6] + \
			   		  "\n                [o] log[7] is: " + material[n][7] + \
			   		  "\n                [o] log[8] is: " + material[n][8] + \
			   		  "\n                [o] log[9] is: " + material[n][9] + \
			   		  "\n                [o] log[10] is: " + material[n][10] + \
			   		  "\n                [o] log[11] is: " + material[n][11] + \
			   		  "\n                [o] log[12] is: " + material[n][12] + \
			   		  "\n                [o] log[13] is: " + material[n][13] + \
			   		  "\n                [o] log[14] is: " + material[n][14] + \
					  "\n                [o] log[15] is: " + material[n][15] + \
					  "\n                [o] log[16] is: " + material[n][16] + \
					  "\n                [o] log[17] is: " + material[n][17] + \
					  "\n                [o] log[18] is: " + material[n][18] + "\n"
		"""
		#處理AppScan要的request cookie，先切好cookie值
		req_cookie = cookie_knife(material[n][8])
		#把處理好的cookie值，丟去包成AppScan要的格式
		req_cookie_wrap = cookie_wrap_up(material[n][17], material[n][16], req_cookie)
		#開始拼湊AppScan的exd格式內容
		"""
		newcontent += "  <request scheme=\"" + material[n][15] + "\" host=\"" + material[n][16] \
		 		   + "\" path=\"" + material[n][17] + "\" port=\"" + material[n][18] \
				   + "\" method=\"" + material[n][6] \
				   + "\" RequestEncoding=\"28591\" SessionRequestType=\"Login\" ordinal=\"\">\n" \
				   + "    <raw encoding=\"none\">" \
				   + material[n][8].replace("\u000d\u000a", "\n").replace("&", "&amp;") \
				   + "    </raw>\n" + req_cookie_wrap + "  </request>\n"
		"""
		newcontent += "  <request scheme=\"" + material[n][15] + "\" host=\"" + material[n][16] \
		 		   + "\" path=\"" + material[n][17] + "\" port=\"" + material[n][18] \
				   + "\" method=\"" + material[n][6] \
				   + "\" RequestEncoding=\"28591\" SessionRequestType=\"Login\" ordinal=\"\">\n" \
				   + "    <raw encoding=\"none\">" \
				   + material[n][8].replace("\u000d\u000a", "\n").replace("&", "&amp;")
		#如果有POST，要塞值進去
		if material[n][9]:
			#print("\n\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
			#print(material[n][9])
			#print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n\n")
			material[n][9] = codecs.decode(material[n][9], "hex")
			newcontent += material[n][9].replace("&", "&amp;") + "\n"
		newcontent +=  "    </raw>\n" + req_cookie_wrap + "  </request>\n"

	#print(newcontent)
	#整個exd檔的前綴文字
	prefix_str = "<?xml version=\"1.0\" encoding=\"utf-16\"?>\n" \
			  + "<!--Automatically created by AppScan at 9/1/2017 12:01:34 PM-->\n" \
			  + "<!--Do NOT Edit!-->\n" \
			  + "<requests>\n"
	#整個exd檔的後綴文字
	postfix_str = "</requests>\n" \
				+ "<!--Number of Requests in file = " + str(len(material)) + "-->"
	#前後綴+request內容
	newcontent = prefix_str + newcontent + postfix_str
	return newcontent


if __name__ == '__main__':
	#設定要看的副檔名
	subfilename_in = ".log"
	subfilename_out = ".exd"
	#讀取同資料夾下，所有副檔名符合條件的檔名
	filenames_arr = [fname for fname in os.listdir("./") if fname.endswith(subfilename_in)]
	#show所有讀到的檔名
	print("\n[+] file list is : " + str(filenames_arr))

	#逐一處理檔案
	for fname in filenames_arr:
		print("\n    [o] Load <<< " + fname)
		#call parse處理檔案內容
		parsed_content = txt_proc(fname)
		#debug是否有抓到檔案內容
		#print("---- ---- ---- ---- ---- ----\n" + str(parsed_content[0][0]) + "\n---- ---- ---- ---- ---- ----\n")
		output_content = compose(parsed_content)
		#寫出至檔案
		fname_out = fname.replace(subfilename_in, subfilename_out)
		outfile = open(fname_out, "wb")
		outfile.write(output_content.encode("utf-16"))
		#debug 檔案寫出
		print("    [>] Output >>> " + fname_out )
		"""
		00: Serial Number	|	32
		01: TimeStamp		|	1504338436245
		02:
		03:
		04: TimeStamp		|	1504338436594
		05: RTT (ms)		|	35
		06: HTTP METHOD		|	GET
		07: URL				|	http://www.runoob.com
		08: Request Header	|	GET http://www.runoob.com HTTP/1.1\\u000d\\u000a...\\u000d\\u000a\\u000d\\u000a
		09: Request Content |
		10: Response Header |
		11: Response Content|
		12: 				|	NULL
		13:
		14: 				|	TRUE/FALSE
		15: scheme			|	https
		16: host			|	www.asd.com
		17: path			|	wp-content/themes/hkjl/user/userinfo.php
		18: port			|	443
		"""

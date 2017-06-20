import base64
import zlib
def base_n(num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyz"):
    return ((num == 0) and "0") or (base_n(num // b, b).lstrip("0") + numerals[num % b])

license='''AAABMg0ODAoPeNqVUUtrAjEQvudXBHreZd2KLwhU1j0orha1LYVexjBq7G6yTBIf/fXNVmlL6cVDQ
ma+fI9J7lYe+cRrniY8aQ/avUHa4dloFepWl43QSlK1U0aLyXgx5IWykr8Yet+U5sjzk0NtA2jfB
jw/QOmhucpmvlojzTdPFsmKqMUywi9kBA5FoxwlnShNmDRVrLQ2gWq28b46YrxXBFEVbKLj1SbCb
5sYpFMHFI48ssxoF+q8AFWKk//YgcEqnB+2zR4HbfaT6UIplQxK+BxiNb2UBa4O4qAl5qda0flXw
m6TcE5b0MpeNF7VGjRb5jMRVjTt9/r3/U739imWDsghiQ2UFtn0Eup//yu4Otc4gwpFNi+KfJGNh
9PbbTGMSjUpe33AR09yBxb//son7Km5cjAsAhQWL0+crJjxU4Lry+aeSiQiAK6QogIULU/4c91F/
Win+cBXW92D9fL9y0Q=X02fb'''

# print ('license length: %s'%len(license))
s = base64.b64decode(license)
t=ord(s[:4].decode('UTF-32BE'))
licenseText, licenseSig = s[4:4 + t], s[4 + t:]
icenseTextOriginal = zlib.decompress(licenseText[5:])
# print (icenseTextOriginal,'icenseTextOriginal')
icenseTextOriginal=icenseTextOriginal.decode()

ExpiryDate="2017-08-23"
textList=icenseTextOriginal.split('\n')
# print ('\n'.join(textList))
for i,text in enumerate(textList):
    if text.find('Evaluation')>=0 and text.find('Description')>=0:
        textList[i]=text.replace('Evaluation','Commercial')
    if text.find('MaintenanceExpiryDate')>=0:
        textList[i]='MaintenanceExpiryDate=%s'%ExpiryDate
    if text.find('LicenseExpiryDate')>=0:
        textList[i]='LicenseExpiryDate=%s'%ExpiryDate
    if text.find('ContactEMail')>=0:
        textList[i]=''
    if text.find('Evaluation=true')>=0:
        textList[i]='Evaluation=false'
textList=[text for text in textList if text!='']

text='\n'.join(textList)
# print (text.encode())


import struct
# f=open('/Users/xz/crack/capture.txt','rb')
# ss=f.read()
ss=text.encode()

size=struct.pack('>L',len(ss))
# print ('size:',size,len(size))
id=struct.pack('bbbbb',13,14,12,10,15)
# print ('id:',id)
gzPrefix=b'\x78\xDA'
# print ('gzPrefix:',gzPrefix)
gzdeflate=zlib.compress(ss,9)
# print ('gzdeflate:',gzdeflate)
# print ('====')
result=size+id+gzdeflate
# print (result)
# print (type(zlib.adler32(ss)))
# print ('======')
new=base64.b64encode(result)
end=base_n(len(new),31)
# print (new,end)
s='%sX02%s'%(new.decode(),end)
print (s)

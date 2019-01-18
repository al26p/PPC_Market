import json


if __name__ == "__main__" :
    fT=open("meteoDataT.txt", 'r')
    fSun=open("meteoDataSun.txt", 'r')
    fF=open("meteoDataF.txt", 'r')

    temp = list()
    sun = list()
    wind = list()

    i=0

    while (i<840) :
        strT = fT.readline()
        strSun = fSun.readline()
        strF = fF.readline()

        strF= strF.strip('\n')
        strT= strT.strip('\n')
        strSun= strSun.strip('\n')

        temp.append(float(strT))
        sun.append(float(strSun))
        wind.append(float(strF))

        i+=1

    fT.close()
    fSun.close()
    fF.close()
    data = {
        "wind" : wind,
        "sun" : sun,
        "temp" : temp
    }
    with open ("meteoData.json", 'w') as out :
        json.dump(data,out)

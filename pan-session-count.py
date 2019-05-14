import requests
import datetime
import time

#** Function to Process API connect **

def get_api_key(ip,username,password):
    url = "https://"+ip+"/api/?type=keygen&user="+username+"&password="+password
    response = requests.get(url,verify=False)
    r = response.text
    r = r[42:-26]
    return(r)

#** Function to get number sessions
def count_session(ip,key):
    url = 'https://'+ip+'/api/?type=op&key='+key+'&cmd=<show><session><info></info></session></show>'
    response = requests.post(url,verify=False)
    r = response.text
    loc1 = r.index('<num-active>')
    loc2 = r.index('</num-active>')
    loc3 = r.index('<cps>')
    loc4 = r.index('</cps>')
    loc5 = r.index('<kbps>')
    loc6 = r.index('</kbps')
    value = {
        "allocated": r[loc1+12:loc2],
        "throughput": r[loc5+6:loc6],
        "newconn": r[loc3+5:loc4]
    }
    return(value)

#Function to write value to a file
def write_number(file,session):
    f = open(file,"a+")
    f.write(session)
    f.close()

#** Input information to log in to Firewall **
ipaddr = input("Firewall IP address: ")
user = input("Username: ")
passwd = input("Password: ")
#destserver = input("Dia chi IP cua Server can monitor session: ")
timelapse = input("Thoi gian lay mau, tinh bang giay (60/120/180/240/300/360/420/480): ")

filename = str(datetime.datetime.now().strftime("%Y-%m-%d")) + "_session_count_" + ".csv"
with open(filename,"w") as f:
    f.write("Date, Time, Allocated, Throughput, NewConnection")

while True:

    k = get_api_key(ipaddr,user,passwd)
    s = count_session(ipaddr,k)
    print(s)
    filename = str(datetime.datetime.now().strftime("%Y-%m-%d")) + "_session_count_" + ".csv"
    write_number(filename,"\n"+str(datetime.datetime.now().strftime("%Y/%m/%d")) + "," + datetime.datetime.now().strftime("%H:%M:%S")+ ","+ s["allocated"] + "," + s["throughput"] + "," + s["newconn"])
    time.sleep(int(timelapse) - (time.time() % int(timelapse)))






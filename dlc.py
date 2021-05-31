# import urllib.request
from typing import Text
import urllib3
import csv

# import requests
from datetime import datetime

# def main():
#     if len(sys.argv)<2:
#         print """Help:
#     Usage:DomainsChecker.py wordlist.txt"""
#         sys.exit(0)
#     wordlist=sys.argv[1]
#     a=open(wordlist,"r").readlines()
#     start_time = time.time()
#     for url in a:
#         if "http" not in url or "https" not in url:
#             url="http://"+str(url)
#         try:
#             response=urllib.urlopen(url).getcode()
#             if response in xrange(200,400) or response in xrange(100,101):
#                 print "["+str(response)+"] "+str(url)
#                 response=requests.get(url)
#                 if response.history:
#                     for res in response.history:
#                         print "\tRedirected To : "+"[Response:"+str(res.status_code)+"] "+str(res.url)
#                     print "\tFinal Redirection : "+"[Response:"+str(response.status_code)+"] "+str(response.url)
#         except IOError:
#             pass
#     print "\n[!]Finished In {} Second(s).".format(int(time.time() - start_time))

# faster = threading.Thread(target=main)
# faster.start()
# faster.join()

filename = input("Please enter filename of list: ")
http = urllib3.PoolManager()
csv_columns = ["URL", "Response_Code", "Status"]
data = []

try:
    with open(filename, "r") as f:
        f_data = f.read().splitlines()
        total = len(f_data)
        print("{0} URLs found.".format(total))
        time_start = datetime.now()

        for index, url in enumerate(f_data):
            # print(url)test.t
            temp = dict()
            if "http" not in url and "https" not in url:
                url = "https://" + str(url)
            elif "http:" in url:
                url = url.replace("http:", "https:")

            try:
                response = http.request("GET", url, timeout=5.0).status
                print()
                if response in range(200, 401) or response in range(100, 101):
                    print(
                        "[{0}/{1}] {2} - {3} ({4})".format(
                            index + 1, total, url, "SUCCESS", str(response)
                        )
                    )
                    temp["URL"] = url
                    temp["Response_Code"] = response
                    temp["Status"] = "SUCCESS"
                    data.append(temp)
                else:
                    print(
                        "[{0}/{1}] {2} - {3} ({4})".format(
                            index + 1, total, url, "FAIL", str(response)
                        )
                    )
                    temp["URL"] = url
                    temp["Response_Code"] = response
                    temp["Status"] = "FAIL"
                    data.append(temp)

            except Exception as e:
                print(
                    "[{0}/{1}] {2} - {3} ({4})".format(
                        index + 1, total, url, "FAIL", "UNREACHABLE"
                    )
                )
                temp["URL"] = url
                temp["Response_Code"] = "UNREACHEABLE"
                temp["Status"] = "FAIL"
                data.append(temp)

        time_end = datetime.now()
        csv_file = datetime.now().strftime("%m%d%Y-%H-%M-%S.csv")
        try:
            with open(csv_file, "w", newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
                writer.writeheader()
                for data in data:
                    writer.writerow(data)

        except IOError:
            print("I/O error")

        print("Results file: {0}".format(csv_file))
        print("Finished in {0} seconds.".format(time_end - time_start))


except Exception as e:
    print(e)

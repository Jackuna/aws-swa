import paramiko
import os
import re
import base64
import json
import logging
from datetime import datetime,timedelta
from timeit import default_timer as timer

paramiko.util.log_to_file("paramiko.log")
logging.basicConfig(filename='paramiko.log', level=logging.DEBUG, filemode='a+', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

dt = datetime.now()
today = dt.strftime('%m%d%y')
download_dict = {today: {}}

def print_data():

    get_list = os.listdir()
    for file in get_list:
            print(file)


def update_record(filename, filestatus, remote_file_size):
    global download_dict
    # Opening JSON file and reading it's content.
    log_filesize = os.path.getsize("todays_file.txt")

    if log_filesize == 0:
        pass
    else:
        with open("todays_file.txt", "r") as read_file:
            #pass
            download_dict = json.load(read_file)
            #print(download_dict[today].keys())

    download_dict[today].update({filename: {'filestatus': filestatus, 'filesize':  remote_file_size}})
    with open("todays_file.txt", "w+") as outfile:
        json.dump(download_dict, outfile)

def remove_old_artifacts(prefix):

    get_cwd = os.getcwd()
    get_list = os.listdir()
    for file in get_list:
        if bool(re.fullmatch(prefix + '[0-9]{4,5}.tar', file)):
            joined_data = get_cwd + "\\" + file
            os.remove(joined_data)
            print("Clean Up Done !")
        else:
            pass

# A call back function for sftp transfers.


def printtotals(transferred, tobetransferred):

    if transferred != tobetransferred:
        print("Downloaded :" + str(transferred)+"/"+str(tobetransferred), end='\r')
    else:
        print("file downloaded ", transferred, "equal to ", tobetransferred)


# Open a transport
def sftp_transport():

    start = timer()
    host, port = "192.168.56.1", 2223
    username, password = 'sftpadmin', 'redhat'
    try:
        # Connect
        transport = paramiko.Transport((host, port))
        # Auth
        decode = base64.b64decode("cmVkaGF0").decode("utf-8")
        transport.connect(None, username, decode)
        # Initiate SFTP
        sftp = paramiko.SFTPClient.from_transport(transport)
        # SFTP Commands
        file_list = sftp.listdir()

        def download_file(remote_get_loc, local_put_loc):

            remotepath = remote_get_loc
            localpath = local_put_loc
            sftp.get(remotepath, localpath, callback=printtotals)

        get_list = os.listdir()
        for file_name in file_list:
            dt = datetime.now()

            prefix = dt.strftime('daily%m%d%y')

            #print(download_dict[today].keys())
            if bool(re.fullmatch(prefix + '[0-9]{4,5}.tar', file_name)) and (file_name not in download_dict[today].keys()):
                print("Downloading file :", file_name)
                transpose_input1 = "/" + file_name
                get_cwd = os.getcwd()
                transpose_input2 = get_cwd + "\\" + file_name
                get_size = str(sftp.lstat(transpose_input1)).rsplit(sep=' ', maxsplit=5)[1]

                try:
                    download_file(transpose_input1, transpose_input2)

                except paramiko.SSHException as sftp_get_exception:
                    print("ERROR while downloading file: msg :", sftp_get_exception)
                    logging.error("error while downloading file: msg : %s " % (sftp_get_exception), exc_info=True)
                finally:

                    expected_file_size = sftp.stat(transpose_input1).st_size
                    downloaded_file_size = os.path.getsize(transpose_input2)
                    if expected_file_size != downloaded_file_size:
                        print("FAILED", "Remote File Size :", expected_file_size, "Local File Size :" ,
                              downloaded_file_size)
                    else:
                        #print(download_dict[today].keys())
                        update_record(file_name, 'downloaded', get_size)
                        print("Downloading Status :", file_name, ": SUCCESS :", "Remote File Size :", expected_file_size, "Local File Size :" ,
                              downloaded_file_size)
                        logging.info("Downloading Status : %s : SUCCESS : Remote File Size : %s Local File Size : %s" % ( file_name,
                        downloaded_file_size, expected_file_size))

            else:

                pass

        # Close SFTP Connection
        if sftp: sftp.close()
        if transport: transport.close()
        end = timer()
        execution_time = str(timedelta(seconds=end - start))
        print("Script Execution time", execution_time)
        logging.info("Script Execution time : %s " %(execution_time))


    except paramiko.SSHException as ssherror:
        print(ssherror)
        logging.error(ssherror)


remove_old_artifacts('daily061421')
sftp_transport()
#print_data()

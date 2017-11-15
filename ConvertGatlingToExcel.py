# install phantomjs
# https://www.joecolantonio.com/2014/10/14/how-to-install-phantomjs/
# http://phantomjs.org/download.html

# pip install selenium

import csv
import os
import subprocess

from selenium import webdriver

path_of_report = "D:/Capacity_50_Users-1508990428221/"

path_of_index = "file:///{}index.html".format(path_of_report)
path_output_file = "{}report.csv".format(path_of_report)

# getting ids of requests from list of files
reguest_ids = [p.replace('.html', '') for p in os.listdir(path_of_report)
               if p.endswith('.html') and p != 'index.html']

driver = webdriver.PhantomJS()
driver.get(path_of_index)

header = driver.find_element_by_id('container_statistics_head').text.split('\n')
# header_of_cvr = ('Requests ' + header[1]).split()
header_of_cvr = [
    'Requests', 'Total', 'OK', 'KO', 'KO-%', 'Req/s',
    'Min', '50th-pct', '75th-pct', '95th-pct', '99th-pct',
    'Max', 'Mean', 'Std-Dev']

total = ['Global-Information'] + header[2].split()[2:]

# write to report.csv
with open(path_output_file, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=header_of_cvr,
                            delimiter=';', lineterminator='\n')
    writer.writeheader()
    writer.writerow(dict(zip(header_of_cvr, total)))
    for reguest_id in reguest_ids:
        data = driver.find_element_by_id(reguest_id).text.split()
        writer.writerow(dict(zip(header_of_cvr, data)))

driver.quit()

cmd = 'start excel {}'.format(path_output_file)
subprocess.call(cmd, shell=True)

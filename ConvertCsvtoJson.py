import csv
import json
import re
def convertCsvtoJson(inCsvFile, outJsonFile):
    with open(inCsvFile) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        line_count = 0
        connections = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            connection = {}
            print("ID: {0}, NAME: {1} {2}, COUNTRY: {3}, INDUSTRY: {4}, DESIGNATION: {5}, EXPERIENCE_SUMMARY: {6}".format(row[0],row[1],row[2],row[3],row[4],row[5],row[6]))
            connection["ID"] = row[0]
            connection["NAME"] = row[1] + " " + row[2]
            connection["COUNTRY"] = row[3]
            connection["INDUSTRY"] = row[4]
            connection["DESIGNATION"] = row[5]
            connection["EXPERIENCE_SUMMARY"] = row[6]
            connections.append(connection)
            line_count += 1
            # if line_count > 5:
            #     break;
        print(f'Processed {line_count} lines.')
        for connection in connections:
            with open(outJsonFile+"."+connection["ID"]+".json", 'w') as outfile:
                json.dump(connection, outfile)
        # with open(outJsonFile, 'w') as outfile:
        #     json.dump(connections, outfile)

def convertCsvtoJson2(inCsvFile, outJsonFile):
    with open(inCsvFile, "r") as csv_file:
        jobs = []
        line_count = 0
        for line in csv_file:
            job = {}
            row = processCsvLine(line)
            if len(row) == 0:
                continue
            if re.match("^[0-9]+.*", row[4]):
                print("Desc: {1}, Title: {0}, URL: {2}, JobID: {3}.".format(row[3], row[5], row[7], row[8]))
                job["Title"] = row[3]
                job["Description"] = row[5]
                job["URL"] = row[7]
                job["JobId"] = row[8]
            else:
                print("Desc: {1}, Title: {0}, URL: {2}, JobID: {3}.".format(row[3], row[5], row[8], row[9]))
                job["Title"] = row[4]
                job["Description"] = row[6]
                job["URL"] = row[8]
                job["JobId"] = row[9]
            jobs.append(job)
            line_count += 1
            # if line_count > 10:
            #     break;
        print(f'Processed {line_count} lines.')
        # alljobs = {"All":jobs}

        for job in jobs:
            with open(outJsonFile+"."+job["JobId"]+".json", 'w') as outfile:
                json.dump(job, outfile)

def processCsvLine(line):
    columns = []
    prev = 0
    start = True
    pos = line.find(',"', 0, -1)
    while pos != -1:
        # print("pos={0}".format(pos))
        prev = pos+2
        if start:
            pos = line.find('",', prev, -1)
            # print("column={0}".format(line[prev:pos]))
            columns.append(line[prev:pos])
            start = False
        else:
            pos = line.find(',"', prev, -1)
            start = True
    #columns.append(line[prev:])
    if len(columns) != 0:
        prev = line.find('https://krb', 0, -1)
        pos = line.find(',', prev+11, -1)
        columns.append(line[prev:pos])
        prev = line.find('jobid=', prev, -1)
        pos = line.find(',', prev+6, -1)
        columns.append(line[prev+6:pos])
        print("Columns: {0}".format(columns))
    return columns

def main():
# convert jobs
#    convertCsvtoJson2("/Users/cc203mr/Downloads/jobs_part_aa", "/Users/cc203mr/Downloads/jobs_part_aa.out")
# convert connections
    convertCsvtoJson("/Users/cc203mr/Downloads/connections/connections_acc_ac", "/Users/cc203mr/Downloads/connections/connections_acc_ac.out")


if __name__ == '__main__':
    main()
#!/usr/bin/env python

#Invoke from terminal with either -u or -r for updating the domain table or generating a report, respectively
#The tables 'mailing' and 'domains' are in the database named 'email'
#The table 'domains' has the following structure: domain VARCHAR(255), date, DATE increase, int
#I have included the mock data I bulk loaded into the database for testing purposes
#During development I made the assumption that all data will be well-formed

from __future__ import division
import argparse
from collections import Counter
from datetime import date
from datetime import timedelta

class DatabaseInterface:
    import MySQLdb;

    def __init__(self):
        try:
            self.db = self.MySQLdb.connect(host="localhost", user="root", passwd="", db="email")
            self.cursor = self.db.cursor()
        except mySQLdb.Error, e:
            print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])

    def getemails(self):
        self.cursor.execute("SELECT * FROM mailing")
        return self.cursor.fetchall()

    def getdomains(self):
        self.cursor.execute("SELECT * FROM domains")
        return self.cursor.fetchall()

    def insertincrease(self, domain, date, increase):
        self.cursor.execute("INSERT INTO domains(domain, date, increase) VALUES('%s', '%s', '%s')" % (domain, date, increase))

    def commit(self):
        self.db.commit()

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--report', action='store_true')
parser.add_argument('-u', '--update', action='store_true')
args = parser.parse_args()       
dbinterface = DatabaseInterface()

def generatereport():
    print "Generating report"

    domain_increases = dbinterface.getdomains()
    domain_totals = Counter()
    month_increase = Counter()

    for domain in domain_increases:
        domain_totals[domain[0]] += domain[2]

        if domain[1] >= date.today() - timedelta(days=30):
            month_increase[domain[0]] += domain[2]

    report = []
    for domain in domain_totals.most_common(50 if 50 <= len(domain_totals) else len(domain_totals)): #If total domains is less than 50 then use all
        report.append([domain[0], domain[1], (month_increase[domain[0]] / domain[1])])

    report.sort(key = lambda x: x[2], reverse=True)
    for domain in report:
        print 'Domain:%s  Count:%s  Percent Increase:%s \n' % (domain[0], domain[1], domain[2])

#Calculates the daily domain count increase by comparing the totals from the mailing and domains tables
def updatedomaintable():
    print "Updating domains table"
    current_domain_count = getmailingtotals()
    old_domain_count = getdomaintotals()

    for domain, count in current_domain_count.iteritems():
        increase = count - old_domain_count[domain]
        dbinterface.insertincrease(domain, date.today(), increase) #possible for increase to be negative, meaning emails were removed
 
    dbinterface.commit()

def getmailingtotals():
    emails = dbinterface.getemails()
    domain_counter = Counter()

    for email in emails:
        domain = email[0].split('@')[1] #Separate domain from email (assumes addresses are well-formed)
        domain_counter[domain] += 1

    return domain_counter

def getdomaintotals():
    domains = dbinterface.getdomains()
    domain_counter = Counter()
    
    for domain in domains:
        domain_counter[domain[0]] += domain[2]

    return domain_counter

def main():
    if args.report == True:
        generatereport()
    if args.update == True:
        updatedomaintable()

if __name__ == "__main__":
    main()

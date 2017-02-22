import glob
import math
import urllib2
import urllib
import csv
import os
import shutil
import urllib2
import csv
import sys

company_list = []

with open('companylist.csv', 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
                company = row[0].split()[0].split(',')[0]
                company = company.split('"')[1]
                #print "Company name:", company

                if "^" not in company:
                        company_list.append(company)

##company_list = [ "TREE", "LULU","MITT^A", "AAPL", "FB", "VIPS", "NOAH"]

for company in company_list:
        revenues_list = []
        earnings_list = []
        bookvalue_list = []
        roic_list = []
        operating_list = []

##        print "Testing Company:", company

        CSV_URL = 'http://financials.morningstar.com/finan/ajax/exportKR2CSV.html?&callback=?&t=XNYS:' + str(company) + '&region=usa&culture=en-US&cur=&order='

        response = urllib2.urlopen(CSV_URL)
        cr = csv.reader(response)


        found_earn = False
        found_rev = False
        found_book = False
        found_roic = False
        found_operating = False
        for row in cr:
                if 'Revenue USD Mil' in row:
                        revenues_list = row[1:]
                        found_rev = True
                if 'Earnings Per Share USD' in row:
                        earnings_list = row[1:]
                        found_earn = True
                if 'Book Value Per Share * USD' in row:
                        bookvalue_list = row[1:]
                        found_book = True
                if 'Return on Invested Capital %' in row:
                        roic_list = row[1:]
                        found_roic = True
                if 'Operating Cash Flow USD Mil' in row:
                        operating_list = row[1:]
                        found_operating = True                        

                if (found_rev and found_earn and found_book and found_operating and found_roic):
                        #print "Values Retrieved"
                        break

        rev_error_bound = 2
        earn_error_bound = 2
        book_error_bound = 2
        roic_error_bound = 2
        operating_error_bound = 2
        rev_error_count = 0
        earn_error_count = 0
        book_error_count = 0
        roic_error_count = 0
        operating_error_count = 0
        num_years = 0
        min_years = 4

        for i in range(len(revenues_list)-2):
                if (revenues_list[i] != '' and earnings_list[i] != '' and operating_list[i] != '' and bookvalue_list[i] != '' and roic_list[i] != '') and (revenues_list[i+1] != '' and earnings_list[i+1] != '' and operating_list[i+1] != '' and bookvalue_list[i+1] != '' and roic_list[i+1] != ''):
                        rev_float = float(revenues_list[i].replace(",", ""))
                        next_rev_float = float(revenues_list[i+1].replace(",", ""))
                        if rev_float*1.10 > next_rev_float:
                                rev_error_count += 1
                                #print('Revenue didnt increase by 10%')
                        if float(earnings_list[i].replace(",", ""))*1.10 > float(earnings_list[i+1].replace(",", "")):
                                earn_error_count += 1
                                #print "Earnings now:", earnings_list[i]
                                #print "Earnings later:", earnings_list[i+1]
                                #print('Earnings didnt increase by 10%')
                        if float(bookvalue_list[i].replace(",", ""))*1.10 > float(bookvalue_list[i+1].replace(",", "")):
                                book_error_count += 1
                                #print('Book Value didnt increase by 10%')
                        if float(roic_list[i]) < 10:
                                roic_error_count += 1
                                #print('ROIC less than 10%')
                        if float(operating_list[i].replace(",", ""))*1.10 > float(operating_list[i+1].replace(",", "")):
                                operating_error_count += 1
##                                print('Operating less than 10%')
                                
                        
                        num_years += 1

        if (num_years >= min_years and operating_error_count <= operating_error_bound and rev_error_count <= rev_error_bound and earn_error_count <= earn_error_bound and book_error_count <= book_error_bound and roic_error_count <= roic_error_bound):
                print "Company Name", company
                print("INVEST")
##        else:
##                print("DONT INVEST")


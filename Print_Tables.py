#!/usr/bin/python
import cx_Oracle
import sys
import sha
import string
import csv
import time
import traceback,sys




########################################################################
class Print_Tables:

	master_db = {}

	def add_table(self, cursor, records, name, tab=1 ):
		""""""
		try:
			heading =  []
			maxlength = [0] * len(cursor.description)
			for row in records:
				for field, index in zip(row, range(len(row))):
					if maxlength [index] < len(str(field)):
						maxlength [index] = len(str(field))
					else:
						maxlength.append(len(str(field)))
				#Init Table Values
			#print maxlength
			widths = []
			columns = []
			tavnit = ' ' * tab + '|'
			separator = ' ' * tab + '+'
			#Info table fiels
			for cd, index in zip(cursor.description,range(len(cursor.description))):
				widths.append(max(maxlength [index], len(cd[0])))
				columns.append(cd[0])
			#Construct Table Index
			for w in widths:
				tavnit += " %-"+"%ss |" % (w,)
				separator += '-'*w + '--+'
			heading.append(separator)
			heading.append(tavnit % tuple(columns))
			heading.append(separator)

			Print_Tables.master_db[name] = {'tavnit': tavnit, 'separator': separator,'heading':heading}

			return True

		except: pass
		return False
	#----------------------------------------------------------------------
	def get_heading(self, name):
		return Print_Tables.master_db[name]['heading']
	#----------------------------------------------------------------------
	def get_separator(self, name):
			return Print_Tables.master_db[name]['separator']
	#----------------------------------------------------------------------
	def get_tavinit(self, name):
		return Print_Tables.master_db[name]['tavnit']


if __name__=='__main__':
	try:
		con = cx_Oracle.connect('hr/hr@192.168.1.104/orcl')
	except cx_Oracle.DatabaseError, exception:
		print exception
		exit(1)

	ptable =  Print_Tables()
	cur = con.cursor()
	cur.execute("SELECT EMPLOYEE_ID as Nome from EMPLOYEES  ")
	results = cur.fetchall()
	ptable.add_table(cur, results, 'employees')
	for t in  ptable.get_heading('employees'): print t
	for row in results:

		print (ptable.get_tavinit('employees') % row)
		print(ptable.get_separator('employees'))
		#example for a second query or more
		#cur2 =  con.cursor()
		#cur2.execute("select JOB_ID , JOB_TITLE, MIN_SALARY, MAX_SALARY FROM JOBS WHERE job_id = '{}'".format(row[3]))
		#results2 = cur2.fetchall()
		#ptable.add_table(cur2, results2, 'jobs', 4)
		#for row2 in results2:
			#for t in  ptable.get_heading('jobs'): print t
			#print (ptable.get_tavinit('jobs') % row2)
		#print(ptable.get_separator('jobs'))
		#cur2.close()
	cur.close()
	con.close()
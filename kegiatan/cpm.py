import csv
import glob
import numpy as np
import os
import pandas as pd
import re
import time


import django
from .models import *
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spkproyeksiumkt.settings")
django.setup()


PATH = "/var/www/html/spkproyeksiumkt/kegiatan/"

class Task(object):
	def __init__(self, nama_kegiatan, kode, predecessor, durasi):
		self.nama_kegiatan = nama_kegiatan
		self.kode = kode.upper()
		self.predecessor = predecessor
		self.durasi = durasi
		self.earlyStart = 0
		self.earliestFinish = 0
		self.successors = []
		self.latestStart = 0
		self.latestFinish = 0
		self.slack = 0
		self.critical = ''

	def computeSlack(self):
		self.slack = self.latestFinish - self.earliestFinish
		if self.slack > 0:
			self.critical = '-'
		else:
			self.critical = 'Kritis'

def readData():
	myfile = PATH + 'data.xlsx'
	sheet = pd.read_excel(myfile, sheet_name='Sheet1')
	return(sheet)

def createTask(mydata):
	taskObject = []

	for i in range(len(mydata)):
		taskObject.append(Task(mydata['Nama Kegiatan'][i], mydata['Kode'][i], mydata['Predecessor'][i], mydata['Durasi'][i]))
	return (taskObject)

def forwardsPass(taskObject):
	for task in taskObject:
		if type(task.predecessor) is str:
			task.predecessor = task.predecessor.upper()
			ef = []
			for j in task.predecessor:
				for t in taskObject:
					if t.kode == j:
						ef.append(t.earliestFinish)
				task.earlyStart = max(ef, default=0)
			del ef
		else:
			task.earlyStart = 0

		task.earliestFinish = task.earlyStart + task.durasi

def backwardsPass(taskObject):
	pred = []
	eF = []

	for task in taskObject:
		if type(task.predecessor) == str:
			for j in task.predecessor:
				pattern = re.compile(r'[A-Z]')
				match = pattern.finditer(j)
				for r in match:
					pred.append(j)
					for m in taskObject:
						if m.kode == j:
							m.successors.append(task.kode)
							# print("successors", m.successors)
							# print("m.successors", m.successors)
		eF.append(task.earliestFinish)

	for task in reversed(taskObject):
		# print("pred", pred)
		if task.kode not in pred:
			task.latestFinish = max(eF)
			# print("task.kode", task.kode, ' is not in predecessor list.', ' The LF is ', task.latestFinish)
			# print("task.latestFinish", task.latestFinish)
		else:
			# print("predecessor list for task.kode ", task.kode, ' is:', task.successors)
			minLs = []
			for x in task.successors:
				# print("task.successors", task.successors)
				for t in (taskObject):
					if t.kode == x:
						# print("t.kode", t.kode)
						# print("task.latestStart", task.latestStart)
						minLs.append(t.latestStart)
						# print("minLs2", minLs)
			task.latestFinish = min(minLs)
			# print("task.latestFinish2", task.latestFinish)
			del minLs

		task.latestStart = task.latestFinish - task.durasi


def slack(taskObject):
	for task in taskObject:
		task.computeSlack()


def updateDataFrame(df, TaskObject):
	df2 = pd.DataFrame({
		'Nama Kegiatan': df['Nama Kegiatan'],
		'Kode': df['Kode'],
		'Predecessor': df['Predecessor'],
		'Durasi': df['Durasi'],
		'ES': pd.Series([task.earlyStart for task in TaskObject]),
		'EF': pd.Series([task.earliestFinish for task in TaskObject]),
		'LS': pd.Series([task.latestStart for task in TaskObject]),
		'LF': pd.Series([task.latestFinish for task in TaskObject]),
		'Slack': pd.Series([task.slack for task in TaskObject]),
		'Lintasan': pd.Series([task.critical for task in TaskObject]),
	})
	return (df2)

def main():
	os.system('clear')
	df = readData()
	# print(df)
	taskObject = createTask(df)
	# print(taskObject)
	forwardsPass(taskObject)
	# print(forwardsPass)
	backwardsPass(taskObject)
	slack(taskObject)
	finaldf = updateDataFrame(df, taskObject)
	print(finaldf)

	print('\nFile saved to data.xlsx\n')
	finaldf.to_csv(PATH + "data.csv", index=False)

	with open(PATH + 'data.csv', 'r', encoding="utf-8") as f:
		reader = csv.DictReader(f)
		for row in reader:
			_, updated = CPM.objects.update_or_create(
				kegiatan=row['Nama Kegiatan'],
				kode=row['Kode'],
				predecessor=row['Predecessor'],
				duration = row['Durasi'],
				earliest_start = row['ES'],
				earliest_finish = row['EF'],
				latest_start = row['LS'],
				latest_finish = row['LF'],
				slack_time = row['Slack'],
				critical = row['Lintasan'],
			)
			# CPM.objects.bulk_create(index_list)

	finaldf.to_excel('data.xlsx', index = False)


# main()





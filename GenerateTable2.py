# Sort the data

from matplotlib import pyplot as plt
import GeneratePDF_Final as pdf

file_hours = "OCDE_Teachers_WorkingHours.csv"
file_salary = "OCDE_Teachers_Salary.csv"
file_students = "OCDE_Teachers_StudentsPerTeacher.csv"

def adding(data):
	global display_data
	for elt in data:
		display_data.append(elt)
	return []

def dataObtention(filename):
	data = readFile(filename)
	data = data.split("\n")
	lines = []
	for line in data:
		l = line.split(",")
		if(len(l) == 8):
			lines.append([l[0], l[2], l[5], l[6]])
	return lines

def dataTreatment(focus):
	if(focus.lower() == "hours"):
		data = dataObtention(file_hours)
	elif(focus.lower() == "salary"):
		data = dataObtention(file_salary)
	elif(focus.lower() == "students"):
		data = dataObtention(file_students)
	else:
		return None
	return data

def defineSubjectFocus():
	f = input("What do you want to focus on ? salary/students/hours: ")
	f = f.lower()
	if(f == "salary" or f == "students" or f == "hours"):
		return f
	else:
		return None

def exiting(*arg):
	return False

def filtering(data):
	focus = input("Which criteria ? country/level/year: ").lower()
	if(focus == "country"):
		focus = input("Which country ? Refer to the abbreviate version: ").upper()
		return filterCountry(data, focus)
	elif(focus == "level"):
		print("If focusing on hours: [PRY/LOWSRY/UPPSRY]")
		print("If focusing on salary: [PRY/LOWSRY/UPPSRY]_[START/15YREXP/TOP]")
		print("If focusing on students: [EARLYCHILDEDU/PRY/SRY/TRY]")
		focus = input("Which level ? ").upper()
		return filterLevel(data, focus)
	elif(focus == "year"):
		focus = input("Which year ? Between 2000 (for some) and 2018: ")
		return filterYear(data, focus)
	else:
		print("Wrong input")
		return data

def filterCountry(data, country):
	filtered_data = []
	for index, elt in enumerate(data):
		if(index == 0 or elt[0] == "{}".format(country)):
			filtered_data.append(elt)
	return filtered_data

def filterLevel(data, level):
	filtered_data = []
	for index, elt in enumerate(data):
		if(index == 0 or elt[1] == "{}".format(level)):
			filtered_data.append(elt)
	return filtered_data

def filterYear(data, year):
	filtered_data = []
	for index, elt in enumerate(data):
		if(index == 0 or elt[2] == "{}".format(year)):
			filtered_data.append(elt)
	return filtered_data

def focusing(data):
	subject_focus = defineSubjectFocus()
	if(subject_focus == None):
		print("Wrong input")
		return data
	raw_data = dataTreatment(subject_focus)
	if(raw_data == None):
		print("Unexpected error, well done! Shouldn't be possible...")
		return data
	return raw_data

def generating(*arg):
	global display_data
	i = 0
	j = 0
	continuer = True
	if(len(display_data) == 0):
		display_data.append(["No data"])
		continuer = False
	elif(len(display_data) == 1):
		continuer = False
	while(continuer):
		if(i == j):
			j += 1
		if(j == len(display_data)):
			i += 1
			j = i + 1
		if(i == len(display_data)-1):
			continuer = False
			continue
		if(display_data[i] == display_data[j]):
			del(display_data[j])
			j -= 1
		if(display_data[i] == ["No data"]):
			del(display_data[i])
		j += 1
	pdf.generatePDF(display_data)
	display_data = []
	return []

def readFile(filename):
	with open(filename, "r") as f:
		data = f.read()
	return data

def wrongSyntax(data):
	print("Wrong input")
	return data

print("Step 1: Focusing\nStep 2: Filtering as much as you want\nStep 3: Adding the filtered data\nStep 4: Go back to Step 1 as much as you want\nStep 5: Generating")
data = []
display_data = []
cases = {"adding": adding, "generating": generating,"filtering": filtering, "focusing": focusing, "exiting": exiting}
while(data != False):
	to_do = input("What to do ? adding/exiting/filtering/focusing/generating: ").lower()
	func = cases.get(to_do, wrongSyntax)
	data = func(data)

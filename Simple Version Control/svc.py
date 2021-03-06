#!/bin/python

'''
		Simple Version Control
		-----------------------
		
		This program stores files needed for version control in 
		a folder named '.svc' in the directory in which it was 
		called.
		The directory structure of '.svc' folder is:
		
		.svc
		|__ changes_file
		|__ recent_file
		
		recent_file stores the most recently commited file
		changes_file stores all the changes made for all commits
		
'''

from sys import argv
import os

COMMIT_ADD_LINE = 0
COMMIT_DELETE_LINE = 1
COMMIT_ERROR = 9

USAGE = "usage: svc <filename> or svc <commit_number>"

'''
	Function name: commit_type
	Parameters:
					old_file_path : The path of the previuosly commited file
					new_file_path : The path of the newly commited file
	Returns:
					( operation_type[, var2, var3] )
					
					operation_type = COMMIT_ERROR	if the commited is invalid
													and var2 and var3 will not be passed
					
					operation_type = COMMIT_ADD_LINE	if the commit contains an added line in the file
														and var2 = index of the added line (0-indexed)
					
					operation_type = COMMIT_DELETE_LINE		if the commit contains a deleted line in the file
															and var2 = index of the deleted line (0-indexed)
																var3 = content of the deleted line
'''
def commit_type(old_file_path, new_file_path):
	old_file_data = open(old_file_path, 'r').read().split('\n')
	new_file_data = open(new_file_path, 'r').read().split('\n')
	if (len(new_file_data)-len(old_file_data)) == 1:
		diff_count = 0
		line_add_index = -1
		old_file_index = 0
		new_file_index = 0
		while old_file_index < len(old_file_data):
			if old_file_data[old_file_index] == new_file_data[new_file_index]:
				old_file_index += 1
				new_file_index += 1
			else:
				line_add_index = new_file_index
				new_file_index += 1
				diff_count += 1
		if diff_count != 1:
			return (COMMIT_ERROR,)
		else:
			return (COMMIT_ADD_LINE, line_add_index)
	elif (len(new_file_data)-len(old_file_data)) == -1:
		diff_count = 0
		line_delete_index = -1
		line_delete_data = ''
		old_file_index = 0
		new_file_index = 0
		while new_file_index < len(new_file_data):
			if old_file_data[old_file_index] == new_file_data[new_file_index]:
				old_file_index += 1
				new_file_index += 1
			else:
				line_delete_index = old_file_index
				line_delete_data = old_file_data[old_file_index]
				old_file_index += 1
				diff_count += 1
		if diff_count != 1:
			return (COMMIT_ERROR,)
		else:
			return (COMMIT_DELETE_LINE, line_delete_index, line_delete_data)		
	else:
		return (COMMIT_ERROR,)



'''
	Function name: main
	Parameters:
					argv: command line arguments passed
	Returns:
					none
	Performes:
					if argv[1] is a file: makes appropriate changes to recent_file and changes_file
					if argv[1] is a number: prints the file commited at number argv[1]
'''
def main(argv):
	if len(argv) != 2:
		print USAGE
		return
	try:
		int(argv[1])
	except:
		root_directory = '.svc'
		if not os.path.exists(root_directory):
			os.makedirs(root_directory)
		recent_file_path = '.svc/recent_file'
		changes_file_path = '.svc/changes_file'
		file_name = argv[1]
		if not os.path.isfile(recent_file_path):
			recent_file = open(recent_file_path,'w')
			recent_file.write(open(file_name,'r').read())
			recent_file.close()
			print 'Initial commit successful'
		else:
			commit = commit_type(recent_file_path, file_name)
			if commit[0] == COMMIT_ADD_LINE:
				changes_file = open(changes_file_path, 'a')
				changes_file.write('-'+str(commit[1])+'\n')
				changes_file.close()
				recent_file = open(recent_file_path,'w')
				recent_file.write(open(file_name,'r').read())
				recent_file.close()
				print 'Commit', len(open(changes_file_path,'r').read().split('\n')[:-1]), 'successful'
			elif commit[0] == COMMIT_DELETE_LINE:
				changes_file = open(changes_file_path, 'a')
				changes_file.write(str(commit[1])+' '+commit[2]+'\n')
				changes_file.close()
				recent_file = open(recent_file_path,'w')
				recent_file.write(open(file_name,'r').read())
				recent_file.close()
				print 'Commit', len(open(changes_file_path,'r').read().split('\n')[:-1]), 'successful'
			elif commit[0] == COMMIT_ERROR:
				print "Invalid commit"
	else:
		recent_file_path = '.svc/recent_file'
		changes_file_path = '.svc/changes_file'

		commit_number = int(argv[1])
		
		try:
			changes_file_data = open(changes_file_path, 'r').read().split('\n')[:-1]
		except:
			open(changes_file_path,'w').close()
			changes_file_data = open(changes_file_path, 'r').read().split('\n')[:-1]

		if commit_number < 0 or commit_number > len(changes_file_data):
			print "Invalid commit number"
		else:
			commit_data = open(recent_file_path,'r').read().split('\n')[:-1]
			for commit in range(len(changes_file_data)-1, commit_number-1, -1):
				current_change = changes_file_data[commit].split(' ',1)
				if current_change[0][0] == '-':
					line_delete_index = int(current_change[0][1:])
					commit_data = commit_data[:line_delete_index] + commit_data[line_delete_index+1:]
				else:
					line_add_index = int(current_change[0])
					commit_data = commit_data[:line_add_index] + [current_change[1]] + commit_data[line_add_index:]
			commit_string = ''
			for commit_data_line in commit_data:
				commit_string += commit_data_line
				commit_string += '\n'
			print commit_string[:-1]
			
if __name__ == '__main__':
	main(argv)

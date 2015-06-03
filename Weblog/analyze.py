import re
from os import system

pattern = '([\d\.]*) - - \[(.*)\] "([^"]*) ([^"]*) ([^"]*)" ([\d-]*) ([\d-]*) "([^"]*)" "([^"]*)"'

'''
	Function name: get_user_agents
	Parameters:
					None
	Performs:
					saves the number of requests per User Agent in file 'html/user_agents.html'
'''
def get_user_agents():
	global pattern
	weblog_data = open('weblog.txt','r').read().split('\n')[:-1]

	user_agent_dict = {}

	for weblog_line in weblog_data:
		line_match = re.match(pattern, weblog_line)
		pattern_browser = '([\w]*)'
		user_agents_match = re.match(pattern_browser, line_match.group(9))

		try:
			user_agent_dict[user_agents_match.group(1)] += 1
		except:
			user_agent_dict[user_agents_match.group(1)] = 1

	total_logs = 0
	for user_agent in user_agent_dict:
		if user_agent != '':
			total_logs += user_agent_dict[user_agent]
	
	replace_string = ''
	for user_agent in user_agent_dict:
		if user_agent != '':
			replace_string += '["' + user_agent + '", ' + str(100*float(user_agent_dict[user_agent])/total_logs) + '],'
			replace_string += '\n'
	
	replaced_data = open('html/base.html','r').read().replace('{{data}}', replace_string)
	replaced_data = replaced_data.replace('{{name}}', 'User Agents Used ')
	open('html/user_agents.html','w').write(replaced_data)

'''
	Function name: get_sites
	Parameters:
					None
	Performs:
					saves the number of requests per site in file 'html/sites.html'
'''

def get_sites():
	global pattern
	weblog_data = open('weblog.txt','r').read().split('\n')[:-1]

	site_dict = {}

	for weblog_line in weblog_data:
		line_match = re.match(pattern, weblog_line)
		pattern_browser = '([^/]*)'
		sites_match = re.match(pattern_browser, line_match.group(4))

		try:
			site_dict[sites_match.group(1)] += 1
		except:
			site_dict[sites_match.group(1)] = 1

	total_logs = 0
	for site in site_dict:
		if site != '':
			total_logs += site_dict[site]
	
	replace_string = ''
	for site in site_dict:
		if site != '':
			replace_string += '["' + site + '", ' + str(100*float(site_dict[site])/total_logs) + '],'
			replace_string += '\n'

	replaced_data = open('html/base.html','r').read().replace('{{data}}', replace_string)
	replaced_data = replaced_data.replace('{{name}}', 'Sites Browsed')
	open('html/sites.html','w').write(replaced_data)

'''
	Function name: get_codes
	Parameters:
					None
	Performs:
					saves the number of requests per Response Codes in file 'html/codes.html'
'''

def get_codes():
	codes = {}
	codes[200] = 'OK'
	codes[206] = 'Partial Content'
	codes[302] = 'Found'
	codes[304] = 'Not Modified'
	codes[404] = 'Not Found'
	codes[500] = 'Internal Server Error'
	global pattern
	weblog_data = open('weblog.txt','r').read().split('\n')[:-1]

	code_dict = {}

	for weblog_line in weblog_data:
		line_match = re.match(pattern, weblog_line)

		try:
			code_dict[line_match.group(6)] += 1
		except:
			code_dict[line_match.group(6)] = 1

	total_logs = 0
	for code in code_dict:
		if code != '':
			total_logs += code_dict[code]
	
	replace_string = ''
	for code in code_dict:
		if code != '':
			replace_string += '["' + codes[int(code)] + '", ' + str(100*float(code_dict[code])/total_logs) + '],'
			replace_string += '\n'

	replaced_data = open('html/base.html','r').read().replace('{{data}}', replace_string)
	replaced_data = replaced_data.replace('{{name}}', 'Response Types')
	open('html/codes.html','w').write(replaced_data)

'''
	Function name: get_dates
	Parameters:
					None
	Performs:
					saves the number of requests per Date in file 'html/dates.html'
'''
def get_dates():
	global pattern
	weblog_data = open('weblog.txt','r').read().split('\n')[:-1]

	date_dict = {}

	for weblog_line in weblog_data:
		line_match = re.match(pattern, weblog_line)
		pattern_browser = '([^:]*):'
		dates_match = re.match(pattern_browser, line_match.group(2))

		try:
			date_dict[dates_match.group(1)] += 1
		except:
			date_dict[dates_match.group(1)] = 1

	total_logs = 0
	for date in date_dict:
		if date != '':
			total_logs += date_dict[date]
	
	replace_string = ''
	for date in date_dict:
		if date != '':
			replace_string += '["' + date + '", ' + str(100*float(date_dict[date])/total_logs) + '],'
			replace_string += '\n'

	replaced_data = open('html/base.html','r').read().replace('{{data}}', replace_string)
	replaced_data = replaced_data.replace('{{name}}', 'Requests by Dates')
	open('html/dates.html','w').write(replaced_data)

get_user_agents()
get_sites()
get_codes()
get_dates()

print "Computed Data, opening results..."

'''
	Opens default browser for displaying results
'''
system('xdg-open html/home.html &> /dev/null')

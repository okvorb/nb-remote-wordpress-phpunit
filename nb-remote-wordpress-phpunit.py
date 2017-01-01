#!/usr/bin/python

import os
import sys
import subprocess
import fileinput

config = {
	 # remote host for accessing via SSH
	"host" 							: "dev.vm",
	 # directory on target machine with wordpress installation for tests running
	"wp_tests_dir" 					: "/var/www/user12345/htdocs/sandbox",
	# directory on target machine to the plugin
	"remote_phpunit_config_dir" 	: "/var/www/user12345/htdocs/wp/wp-content/plugins/user12345-plugin",
	# directory on host machine to the plugin
	"local_phpunit_config_dir" 		: "/home/user12345/Projects/user12345-plugin"
}

def getArgsForPhpUnit() :
	phpunit_args = []
	for index, arg in enumerate(sys.argv, start=1):
		if arg == '--colors' :
			phpunit_args.append(arg)
		elif arg == '--log-json' :
			phpunit_args.append(arg)
			phpunit_args.append(sys.argv[index])
		elif arg == '--coverage-clover' :
			phpunit_args.append(arg)
			phpunit_args.append(sys.argv[index])
	return phpunit_args

def getArgValueByName(name)	:
	for index, arg in enumerate(sys.argv, start=1):
		if arg == name :
			return sys.argv[index]
	return ""	
	
def getTestResultsFile() :
	return getArgValueByName('--log-json')
	
def getCoverageReportFile() :
	return getArgValueByName('--coverage-clover')
	
def getTestToRun() :
	return getArgValueByName('--').replace("--run=", "").replace(config["local_phpunit_config_dir"], "").strip("/")

def getResultsFromRemote():
	log = getTestResultsFile()
	if log :
		os.system("scp {0}:{1} {1}".format(config["host"], log))
	
	coverage = getCoverageReportFile()
	if coverage :
		search = config["remote_phpunit_config_dir"]
		replace = config["local_phpunit_config_dir"]
		os.system("scp {0}:{1} {1}".format(config["host"], coverage))
		for line in fileinput.input(coverage, inplace=True):
			  print line.replace(search, replace)

def runTestsViaSSH():
	host = config["host"]
	phpunit_config_dir = config["remote_phpunit_config_dir"]
	wp_tests_dir = config["wp_tests_dir"]
	args = getArgsForPhpUnit()
	args.append(getTestToRun())
	phpunit_args = " ".join(args)
	subprocess.call(["ssh", host, "cd {0}; WP_TESTS_DIR={1} phpunit {2}".format(phpunit_config_dir, wp_tests_dir, phpunit_args)])
	getResultsFromRemote()
		

runTestsViaSSH()

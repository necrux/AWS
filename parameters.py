# -*- coding: UTF-8 -*-

import os
import json
import textwrap
from sys import argv

def usage():
  print textwrap.dedent("""\

    This script will generate a skeleton parameters file given a CloudFormation template.
    The parameters file will be generated in you current working directory with the name <TEMPLATE>.parameters.

    SYNTAX
       parameters <TEMPLATE>

    USAGE with AWS CLI
       aws cloudformation create-stack --stack-name <MY_STACK> --template-url https://<S3_TEMPLATE_URL> --parameters file://<PARAMETERS_FILE>

    """)

#Basic input validation.  
if len(argv) == 1:
  usage()
  exit(1) 
elif not os.path.isfile(argv[1]):
  usage()
  print "File '%s' does not exists." % (argv[1])
  exit(1)

#Open specified file, verify format, and load it as JSON.
input_file = open(argv[1], 'r')
try:
  json_file = json.load(input_file)
except ValueError:
  usage(1)
  print "Are you sure this is a properly formatted JSON file?"
  exit(1)
input_file.close

#Opening output file. If file exists it WILL be overwritten.
output_file_name = argv[1] + ".parameters"
output_file = open(output_file_name, 'w+')
output_file.write('[\r\n')

#Setting up a count to increment within the for loop. This determines when to stop appending a comma.
count = 0
key_length = len(json_file['Parameters'].keys())

#Output file generation.
for parameter in json_file['Parameters'].keys():
  count += 1
  output_file.write('  {\r\n    "ParameterKey": "%s",\r\n' % (parameter))
  if 'Default' in json_file['Parameters'][parameter]:
    default = json_file['Parameters'][parameter]['Default']
    if count < key_length:
      output_file.write('    "ParameterValue": "%s"\r\n  },\r\n' % (default))
    else:
      output_file.write('    "ParameterValue": "%s"\r\n  }\r\n' % (default))
  else:
    if count < key_length:
      output_file.write('    "ParameterValue": ""\r\n  },\r\n')
    else:
      output_file.write('    "ParameterValue": ""\r\n  }\r\n')

output_file.write(']\r\n')
print "Sucess! The parameters file can be found at: %s" % (os.path.realpath(output_file_name))

#Closing the file for good measure.
output_file.close()

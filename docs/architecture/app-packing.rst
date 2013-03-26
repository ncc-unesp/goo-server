Application Packing
===================

Structure
---------

bin/ : *recommended*
  binaries (and scripts) from application

lib/ : *recommended when necessary*
  libraries required for executing the application

data/ : *recommended when necessary*
  application required databases

hooks/ : *mandatory*
  goo execution scripts

tests/ : *recommended*
  application deployment tests

etc/ : *recommended when necessary*
  other configuration files

Hooks
^^^^^

hooks/execute
  Execution script. Should return only at the end of execution.
  Return code 0 if successfully executed, any number if otherwise.

hooks/checkpoit : **NOT IMPLEMENTED**
  TBD

hooks/progress
  Progress information. Must print to STDOUT two line: the first a Integer from 0 to 100 and the second a ETA, a estimated time to complete execution, in seconds.
  If unable to output the correct information, must return a code different from 0.
    
hooks/log
  Output some relevant information about the progress of the execution. For example a 'tail -n 30' from the correct log file.
  *Must be limitated to 100 lines or 6KB*
  Must return a code different from 0 if unable to output usefull information.

hooks/test
  Execute the deployment tests.
  The tests shouldn't take more than 1 minute to execute in a regular system.
  The test is responsable to control the maximum execution time.
  Must return 0 if OK, any other code if otherwise.


Procudure
---------

Include bin/ (if exists) in PATH
Include lib/ (if exists) in LD_LIBRARY_PATH
Source etc/source.sh (if exists)

Export GOO_HOSTS, GOO_PPH and GOO_JOB_NAME.

Execute 'hooks/execute $ARGS'

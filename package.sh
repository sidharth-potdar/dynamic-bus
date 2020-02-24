this=$(pwd)/$(dirname $0)
cd ../ 
rm -r CX4230_EXPORT 
rm CX4230_EXPORT.zip 
mkdir CX4230_EXPORT 
cp -vr $this/db_logging CX4230_EXPORT/db_logging
cp -vr $this/distributions CX4230_EXPORT/distributions
cp -vr $this/engine CX4230_EXPORT/engine 
cp -vr $this/event_processes CX4230_EXPORT/event_processes
cp -vr $this/events CX4230_EXPORT/events 
cp -vr $this/pickles CX4230_EXPORT/pickles
cp -vr $this/planners CX4230_EXPORT/planners 
cp -vr $this/scheduler CX4230_EXPORT/scheduler
cp -v $this/__init__.py CX4230_EXPORT/__init__.py 
cp -v $this/main.py CX4230_EXPORT/main.py 
cp -v $this/main.sh CX4230_EXPORT/main.sh 
cp -v $this/README.md CX4230_EXPORT/README.md
rm -v CX4230_EXPORT/db_logging/simlog.db 

zip -r CX4230_EXPORT CX4230_EXPORT
# rm -r CX4230_EXPORT
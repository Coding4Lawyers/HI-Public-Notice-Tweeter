# HI-Public-Notice-Tweeter
 HI Public Notice Tweeter

## Setup
 ```
 python -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
 python main.py
 ```
 Cronjob
 ```
 0 14 * * * /home/ubuntu/Honolulu-PD-Arrest-Reports/venv/bin/python /home/ubuntu/Honolulu-PD-Arrest-Reports/main.py > /home/ubuntu/Honolulu-PD-Arrest-Reports/cronlog.log 2>&1
 ```
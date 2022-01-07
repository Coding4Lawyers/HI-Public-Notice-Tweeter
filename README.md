# HI-Public-Notice-Tweeter
 HI Public Notice Tweeter

## Setup
```
git clone git@github.com:Coding4Lawyers/HI-Public-Notice-Tweeter.git
cd HI-Public-Notice-Tweeter
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```
## Cronjob
```
0 13 * * * /home/ubuntu/HI-Public-Notice-Tweeter/venv/bin/python /home/ubuntu/HI-Public-Notice-Tweeter/public_notice_tweet.py > /home/ubuntu/HI-Public-Notice-Tweeter/cronlog.log 2>&1
```

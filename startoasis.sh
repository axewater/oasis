# /bin/bash
cd /var/www/oasis
source venv/bin/activate
nohup python3 app.py &

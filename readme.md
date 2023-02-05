cd /api code
```
python3 -m venv .env
pip install flask

to start the api,

. .env/bin/activate 
python3 delivery_fee_api.py
```

to test the api, open another terminal
```
cd /test_cases
. .env/bin/activate 
python3 -m unittest tests.py

after the tests have passed, we can make request by the client by this command

    python3 client.py
```   

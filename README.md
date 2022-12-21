## Stateful ML Application
This directory contains a stateful ML application that shares both a model and performance metric across a flask application with multiple gunicorn workers using the multiprocess manager dictionary. 

Start app:
```bash
./run.sh
```

Make prediction:
```bash
curl -X POST -H 'Content-Type: application/json' localhost:8080/predict -d '{"x": {"empty_server_form_handler": 1.0, "popup_window": 0.0, "https": 1.0, "request_from_other_domain": 0.0, "anchor_from_other_domain": 1.0, "is_popular": 0.0,"long_url": 0.0, "age_of_domain": 1, "ip_in_url": 0}}'
```

Update model and get the latest AUC:
```bash
curl -X PUT -H 'Content-Type: application/json' localhost:8080/feedback -d '{"x": {"empty_server_form_handler": 1.0, "popup_window": 0.0, "https": 1.0, "request_from_other_domain": 0.0, "anchor_from_other_domain": 1.0, "is_popular": 0.0, "long_url": 0.0, "age_of_domain": 1, "ip_in_url": 0}, "y": 0}'
```

Build and push the image:
```bash
docker build -t kylegallatin/stateful-ml-app .
docker run -p 8080:8080 -it kylegallatin/stateful-ml-app 
``` 
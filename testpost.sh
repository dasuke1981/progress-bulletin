#!/bin/sh

curl -X POST "http://127.0.0.1:8000/add_progress/" -d "id=1000&title=Sample Task&current=50&max_value=100"

#! /bin/bash

curl --request POST http://127.0.0.1:5000/api/timeline_post -d 'name=test&email=test@gmail.com&content=testcontent'

curl --request GET http://127.0.0.1:5000/api/timeline_post

curl --request DELETE http://127.0.0.1:5000/api/timeline_post/

# if any errors occur during requests they will be echoed to shell

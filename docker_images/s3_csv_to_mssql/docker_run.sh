#!/usr/bin/env bash

docker run -e AWS_ACCESS_KEY_ID=PSFBSAZRLHBIHOPNJCJGAFABONEOBNAAHFJBHBPLKL -e AWS_SECRET_ACCESS_KEY=3C1F17195700d1e4d/b7a4FC517EB76d574f79CCNI -e ENDPOINT_URL=http://10.225.112.70 -e BUCKET=mssql-2022-demo-raw -e SERVER=10.225.115.37 -e DATABASE=pds -e USERNAME=sa -e PASSWORD=%greenjam99! s3_csv_to_mssql:1.0

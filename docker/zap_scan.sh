#!/bin/bash
# Simple script to run ZAP docker baseline against local app
docker run --rm -v $(pwd)/zap_reports:/zap/wrk:rw owasp/zap2docker-stable zap-baseline.py -t http://host.docker.internal:5000 -r zap_report.html

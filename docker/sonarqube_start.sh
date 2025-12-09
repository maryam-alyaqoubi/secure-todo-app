#!/bin/bash
docker-compose up -d sonarqube db
echo "SonarQube should be available at http://localhost:9000 (may take 1-2 minutes to initialize)"

#!/bin/bash
# Run OWASP Dependency-Check in docker (requires dependency-check image)
docker run --rm -v $(pwd):/src owasp/dependency-check:latest --scan /src --format ALL --out /src/reports

#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting SonarQube Code Analysis...${NC}"

# Ensure SonarQube is running
echo -e "${YELLOW}📦 Starting SonarQube server...${NC}"
docker-compose up -d sonarqube

# Function to check if SonarQube is ready
check_sonarqube_ready() {
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if curl -s http://localhost:9000/api/system/status | grep -q '"status":"UP"'; then
            return 0
        fi
        echo -e "${YELLOW}⏳ Waiting for SonarQube to be ready... (attempt $attempt/$max_attempts)${NC}"
        sleep 10
        ((attempt++))
    done
    return 1
}

# Wait for SonarQube to be ready
echo -e "${YELLOW}⌛ Checking SonarQube readiness...${NC}"
if check_sonarqube_ready; then
    echo -e "${GREEN}✅ SonarQube is ready!${NC}"
else
    echo -e "${RED}❌ SonarQube failed to start within expected time. Please check the logs.${NC}"
    docker-compose logs sonarqube
    exit 1
fi

# Run the scan
echo -e "${BLUE}🔍 Starting code analysis...${NC}"
docker-compose --profile scan up sonar-scanner

# Check if scan completed successfully
if [ $? -eq 0 ]; then
    echo -e "${GREEN}🎉 Code analysis completed successfully!${NC}"
    echo -e "${GREEN}📊 View your results at: http://localhost:9000${NC}"
    echo -e "${BLUE}📋 Project: $(grep sonar.projectName sonar-project.properties | cut -d'=' -f2)${NC}"
else
    echo -e "${RED}❌ Code analysis failed. Check the logs above for details.${NC}"
    exit 1
fi

# Clean up scanner container
echo -e "${YELLOW}🧹 Cleaning up scanner container...${NC}"
#docker-compose --profile scan down

echo -e "${GREEN}✨ All done! Happy coding!${NC}"

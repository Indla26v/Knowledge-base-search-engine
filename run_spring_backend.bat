@echo off
echo Starting Spring Boot Backend...
echo.

set JAVA_HOME=%~dp0tools\jdk\jdk-17.0.19+10
set PATH=%JAVA_HOME%\bin;%~dp0tools\maven\apache-maven-3.9.6\bin;%PATH%

cd spring-backend
mvn spring-boot:run

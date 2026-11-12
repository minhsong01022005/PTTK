@echo off
rem Chay GaraMan: bat Laragon (MySQL) truoc, sau do chay file nay.
set "JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-17.0.21.9-hotspot"
set "CATALINA_HOME=C:\Users\Admin\tomcat9\apache-tomcat-9.0.98"

set "MAVEN_HOME=D:\BTL\tools\apache-maven-3.9.16"

rem Build lai WAR bang Maven
echo Dang build bang Maven...
pushd "%~dp0"
call "%MAVEN_HOME%\bin\mvn.cmd" -q clean package -DskipTests
if errorlevel 1 (
  echo BUILD LOI! Kiem tra lai code.
  popd
  pause
  exit /b 1
)
popd

rem Chep WAR moi sang Tomcat
if exist "%~dp0target\GaraMan.war" copy /Y "%~dp0target\GaraMan.war" "%CATALINA_HOME%\webapps\" >nul

call "%CATALINA_HOME%\bin\startup.bat"
echo Cho Tomcat khoi dong...
timeout /t 12 /nobreak >nul
start http://localhost:8081/GaraMan/

@echo off
REM OWASP Juice Shop Penetration Testing Suite
REM Docker Quick Start Script for Windows

setlocal enabledelayedexpansion

echo 🐳 OWASP Juice Shop Penetration Testing Suite - Docker Setup
echo ==============================================================

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop:
    echo    https://docs.docker.com/desktop/windows/
    exit /b 1
)

REM Check if Docker Compose is available
docker-compose --version >nul 2>&1
if errorlevel 1 (
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo ❌ Docker Compose is not available.
        exit /b 1
    )
)

if "%1"=="" goto :show_usage
if "%1"=="help" goto :show_usage
if "%1"=="--help" goto :show_usage
if "%1"=="-h" goto :show_usage

if "%1"=="build" goto :build_image
if "%1"=="up" goto :start_containers
if "%1"=="start" goto :start_containers
if "%1"=="test" goto :run_automated_test
if "%1"=="auto" goto :run_automated_test
if "%1"=="interactive" goto :run_interactive
if "%1"=="shell" goto :run_interactive
if "%1"=="logs" goto :show_logs
if "%1"=="down" goto :stop_containers
if "%1"=="stop" goto :stop_containers
if "%1"=="clean" goto :clean_all
if "%1"=="status" goto :show_status

echo ❌ Unknown command: %1
goto :show_usage

:show_usage
echo.
echo Usage: docker-setup.bat [COMMAND]
echo.
echo Commands:
echo   build       Build the penetration testing Docker image
echo   up          Start Juice Shop and penetration testing suite
echo   test        Run automated penetration test
echo   interactive Run in interactive mode for manual testing
echo   logs        Show logs from containers
echo   down        Stop and remove containers
echo   clean       Remove containers, images, and volumes
echo   status      Show status of containers
echo.
echo Examples:
echo   docker-setup.bat up           # Start both Juice Shop and pentest suite
echo   docker-setup.bat test         # Run automated penetration test
echo   docker-setup.bat interactive  # Interactive testing mode
echo.
goto :end

:build_image
echo 🔨 Building penetration testing Docker image...
docker build -t pentest-suite:latest .
if errorlevel 1 (
    echo ❌ Build failed!
    exit /b 1
)
echo ✅ Build completed!
goto :end

:start_containers
echo 🚀 Starting OWASP Juice Shop and Penetration Testing Suite...
docker-compose up -d juice-shop
if errorlevel 1 (
    echo ❌ Failed to start Juice Shop!
    exit /b 1
)

echo ⏳ Waiting for Juice Shop to be ready...
timeout /t 15 /nobreak > nul

echo 🔍 Starting penetration testing suite...
docker-compose up -d pentest-suite
if errorlevel 1 (
    echo ❌ Failed to start pentest suite!
    exit /b 1
)

echo.
echo ✅ Containers started successfully!
echo    • Juice Shop: http://localhost:3000
echo    • ZAP Interface: http://localhost:8080
echo.
echo Next steps:
echo    docker-compose exec pentest-suite python docker_runner.py --interactive
echo    docker-compose logs -f pentest-suite
goto :end

:run_automated_test
echo 🤖 Running automated penetration test...
docker-compose up -d
timeout /t 10 /nobreak > nul
docker-compose exec -e RUN_AUTOMATED_TEST=true pentest-suite python docker_runner.py
echo.
echo 📊 Test completed! Check results:
echo    docker-compose exec pentest-suite ls -la /app/results/
goto :end

:run_interactive
echo 🎮 Starting interactive penetration testing mode...
docker-compose up -d
timeout /t 5 /nobreak > nul
docker-compose exec pentest-suite python docker_runner.py --interactive
goto :end

:show_logs
echo 📋 Showing container logs...
docker-compose logs -f
goto :end

:stop_containers
echo 🛑 Stopping containers...
docker-compose down
echo ✅ Containers stopped!
goto :end

:clean_all
echo 🧹 Cleaning up containers, images, and volumes...
docker-compose down -v --rmi all
docker system prune -f
echo ✅ Cleanup completed!
goto :end

:show_status
echo 📊 Container Status:
echo ===================
docker-compose ps
echo.
echo 🌐 Service URLs:
echo ===============
echo • Juice Shop: http://localhost:3000
echo • ZAP Interface: http://localhost:8080
echo.
echo 💾 Docker Images:
echo ================
docker images | findstr /i "pentest juice zap"
goto :end

:end
endlocal

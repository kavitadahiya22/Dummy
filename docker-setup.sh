#!/bin/bash

# OWASP Juice Shop Penetration Testing Suite
# Docker Quick Start Script

set -e

echo "🐳 OWASP Juice Shop Penetration Testing Suite - Docker Setup"
echo "=============================================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

# Function to show usage
show_usage() {
    echo ""
    echo "Usage: ./docker-setup.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build       Build the penetration testing Docker image"
    echo "  up          Start Juice Shop and penetration testing suite"
    echo "  test        Run automated penetration test"
    echo "  interactive Run in interactive mode for manual testing"
    echo "  logs        Show logs from containers"
    echo "  down        Stop and remove containers"
    echo "  clean       Remove containers, images, and volumes"
    echo "  status      Show status of containers"
    echo ""
    echo "Examples:"
    echo "  ./docker-setup.sh up           # Start both Juice Shop and pentest suite"
    echo "  ./docker-setup.sh test         # Run automated penetration test"
    echo "  ./docker-setup.sh interactive  # Interactive testing mode"
    echo ""
}

# Function to build Docker image
build_image() {
    echo "🔨 Building penetration testing Docker image..."
    docker build -t pentest-suite:latest .
    echo "✅ Build completed!"
}

# Function to start containers
start_containers() {
    echo "🚀 Starting OWASP Juice Shop and Penetration Testing Suite..."
    docker-compose up -d juice-shop
    
    echo "⏳ Waiting for Juice Shop to be ready..."
    sleep 15
    
    # Check if Juice Shop is ready
    if curl -f http://localhost:3000 &> /dev/null; then
        echo "✅ Juice Shop is ready at http://localhost:3000"
    else
        echo "⚠️  Juice Shop might still be starting up..."
    fi
    
    echo "🔍 Starting penetration testing suite..."
    docker-compose up -d pentest-suite
    
    echo ""
    echo "✅ Containers started successfully!"
    echo "   • Juice Shop: http://localhost:3000"
    echo "   • ZAP Interface: http://localhost:8080"
    echo ""
    echo "Next steps:"
    echo "   docker-compose exec pentest-suite python docker_runner.py --interactive"
    echo "   docker-compose logs -f pentest-suite"
}

# Function to run automated test
run_automated_test() {
    echo "🤖 Running automated penetration test..."
    
    # Make sure containers are running
    docker-compose up -d
    
    # Wait a bit for services to be ready
    sleep 10
    
    # Run automated test
    docker-compose exec -e RUN_AUTOMATED_TEST=true pentest-suite python docker_runner.py
    
    echo ""
    echo "📊 Test completed! Check results:"
    echo "   docker-compose exec pentest-suite ls -la /app/results/"
}

# Function to run interactive mode
run_interactive() {
    echo "🎮 Starting interactive penetration testing mode..."
    
    # Make sure containers are running
    docker-compose up -d
    
    # Wait a bit for services to be ready
    sleep 5
    
    # Run interactive mode
    docker-compose exec pentest-suite python docker_runner.py --interactive
}

# Function to show logs
show_logs() {
    echo "📋 Showing container logs..."
    docker-compose logs -f
}

# Function to stop containers
stop_containers() {
    echo "🛑 Stopping containers..."
    docker-compose down
    echo "✅ Containers stopped!"
}

# Function to clean everything
clean_all() {
    echo "🧹 Cleaning up containers, images, and volumes..."
    docker-compose down -v --rmi all
    docker system prune -f
    echo "✅ Cleanup completed!"
}

# Function to show status
show_status() {
    echo "📊 Container Status:"
    echo "==================="
    docker-compose ps
    
    echo ""
    echo "🌐 Service URLs:"
    echo "==============="
    echo "• Juice Shop: http://localhost:3000"
    echo "• ZAP Interface: http://localhost:8080"
    
    echo ""
    echo "💾 Docker Images:"
    echo "================"
    docker images | grep -E "(pentest|juice|zap)"
}

# Main script logic
case "${1:-help}" in
    build)
        build_image
        ;;
    up|start)
        start_containers
        ;;
    test|auto)
        run_automated_test
        ;;
    interactive|shell)
        run_interactive
        ;;
    logs)
        show_logs
        ;;
    down|stop)
        stop_containers
        ;;
    clean)
        clean_all
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        echo "❌ Unknown command: $1"
        show_usage
        exit 1
        ;;
esac

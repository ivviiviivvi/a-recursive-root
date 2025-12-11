#!/bin/bash
# AI Council System - DigitalOcean Quick Deploy
# Automated setup script for Ubuntu 22.04 droplet

set -e

echo "=================================================="
echo "AI Council System - DigitalOcean Deployment"
echo "=================================================="
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   log_error "This script must be run as root (use sudo)"
   exit 1
fi

# Step 1: System Update
log_info "Updating system packages..."
apt-get update -qq
apt-get upgrade -y -qq
log_info "✓ System updated"

# Step 2: Install Docker
log_info "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl enable docker
    systemctl start docker
    log_info "✓ Docker installed"
else
    log_info "✓ Docker already installed"
fi

# Step 3: Install Docker Compose
log_info "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    log_info "✓ Docker Compose installed"
else
    log_info "✓ Docker Compose already installed"
fi

# Step 4: Install Python 3.11
log_info "Installing Python 3.11..."
apt-get install -y software-properties-common
add-apt-repository -y ppa:deadsnakes/ppa
apt-get update -qq
apt-get install -y python3.11 python3.11-venv python3.11-dev python3-pip
log_info "✓ Python 3.11 installed"

# Step 5: Clone Repository
log_info "Cloning AI Council System repository..."
INSTALL_DIR="/opt/ai-council-system"
if [ -d "$INSTALL_DIR" ]; then
    log_warn "Directory already exists, pulling latest changes..."
    cd $INSTALL_DIR
    git pull
else
    git clone https://github.com/your-org/ai-council-system.git $INSTALL_DIR
    cd $INSTALL_DIR
fi
log_info "✓ Repository cloned"

# Step 6: Environment Configuration
log_info "Setting up environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    log_warn "Please edit .env file with your API keys:"
    log_warn "  nano $INSTALL_DIR/.env"
    log_warn ""
    log_warn "Required keys:"
    log_warn "  - ANTHROPIC_API_KEY"
    log_warn "  - OPENAI_API_KEY"
    log_warn ""

    # Prompt for API keys
    read -p "Do you want to enter API keys now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter Anthropic API Key: " ANTHROPIC_KEY
        read -p "Enter OpenAI API Key: " OPENAI_KEY

        sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$ANTHROPIC_KEY/" .env
        sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$OPENAI_KEY/" .env

        log_info "✓ API keys configured"
    fi
else
    log_info "✓ .env file already exists"
fi

# Step 7: Install Dependencies
log_info "Installing Python dependencies..."
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
log_info "✓ Dependencies installed"

# Step 8: Initialize Database
log_info "Initializing database..."
docker-compose -f docker/docker-compose.yml up -d postgres redis
sleep 10  # Wait for DB to be ready
python -c "from core.database import init_db; init_db()"
log_info "✓ Database initialized"

# Step 9: Configure Systemd Service
log_info "Creating systemd service..."
cat > /etc/systemd/system/ai-council.service << EOF
[Unit]
Description=AI Council System
After=network.target docker.service
Requires=docker.service

[Service]
Type=simple
User=root
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$INSTALL_DIR/venv/bin/python -m core.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ai-council
log_info "✓ Systemd service created"

# Step 10: Configure Nginx (Reverse Proxy)
log_info "Installing and configuring Nginx..."
apt-get install -y nginx
cat > /etc/nginx/sites-available/ai-council << 'EOF'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
EOF

ln -sf /etc/nginx/sites-available/ai-council /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
systemctl enable nginx
log_info "✓ Nginx configured"

# Step 11: Configure Firewall
log_info "Configuring firewall..."
ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
log_info "✓ Firewall configured"

# Step 12: Start Services
log_info "Starting AI Council System..."
docker-compose -f docker/docker-compose.yml up -d
systemctl start ai-council
log_info "✓ Services started"

# Step 13: Verify Installation
log_info "Verifying installation..."
sleep 5
if curl -f http://localhost:8000/api/v1/health > /dev/null 2>&1; then
    log_info "✓ Health check passed"
else
    log_warn "Health check failed - services may still be starting"
fi

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo "=================================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=================================================="
echo ""
echo "🌐 Access your AI Council System at:"
echo "   http://$PUBLIC_IP"
echo ""
echo "📊 Dashboard:"
echo "   http://$PUBLIC_IP/dashboard"
echo ""
echo "📚 API Documentation:"
echo "   http://$PUBLIC_IP/docs"
echo ""
echo "🔧 Management Commands:"
echo "   systemctl status ai-council    # Check status"
echo "   systemctl restart ai-council   # Restart service"
echo "   systemctl logs -f ai-council   # View logs"
echo ""
echo "🗄️  Database & Cache:"
echo "   docker-compose -f $INSTALL_DIR/docker/docker-compose.yml ps"
echo ""
echo "📝 Next Steps:"
echo "   1. Verify API keys in $INSTALL_DIR/.env"
echo "   2. Run a test debate: cd $INSTALL_DIR && ./ai-council demo"
echo "   3. Configure SSL certificate (recommended for production)"
echo "   4. Set up monitoring and backups"
echo ""
echo "📖 Full documentation:"
echo "   https://github.com/your-org/ai-council-system"
echo ""
echo "=================================================="

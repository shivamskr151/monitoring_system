#!/usr/bin/env python3
"""
External Authentication Backend for MediaMTX

This backend handles authentication requests from MediaMTX when using external authentication.
MediaMTX will send POST requests to this endpoint for user authentication and authorization.

Usage:
1. Update mediamtx.yml to point to this backend:
   authHTTPAddress: http://your-backend:8000/mediamtx/auth

2. Run this backend:
   python external-authentication-backend.py

3. Restart MediaMTX to apply the new configuration
"""

from flask import Flask, request, jsonify
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Example user database - replace with your actual user management system
USERS = {
    "admin": {
        "password": "admin123",  # In production, use hashed passwords
        "permissions": ["read", "publish", "api", "metrics", "playback"],
        "ips": [],  # Empty means allow from any IP
        "role": "admin"
    },
    "viewer": {
        "password": "viewer123",
        "permissions": ["read", "playback"],
        "ips": [],
        "role": "viewer"
    },
    "guest": {
        "password": "guest123", 
        "permissions": ["read"],
        "ips": [],
        "role": "guest"
    },
    "streamer": {
        "password": "streamer123",
        "permissions": ["read", "publish", "playback"],
        "ips": [],
        "role": "streamer"
    }
}

def authenticate_user(username, password, ip, action, path):
    """
    Authenticate user and check permissions.
    
    Args:
        username: Username from MediaMTX
        password: Password from MediaMTX
        ip: Client IP address
        action: Requested action (read, publish, api, metrics, etc.)
        path: MediaMTX path being accessed
        
    Returns:
        tuple: (is_authenticated, has_permission, user_info)
    """
    # Check if user exists
    if username not in USERS:
        logger.warning(f"Authentication failed: user '{username}' not found from IP {ip}")
        return False, False, None
    
    user = USERS[username]
    
    # Check password
    if user["password"] != password:
        logger.warning(f"Authentication failed: invalid password for user '{username}' from IP {ip}")
        return False, False, None
    
    # Check IP restrictions (if any)
    if user["ips"] and ip not in user["ips"]:
        logger.warning(f"Authentication failed: IP {ip} not allowed for user '{username}'")
        return False, False, None
    
    # Check permissions
    if action not in user["permissions"]:
        logger.warning(f"Permission denied: user '{username}' lacks permission for action '{action}' on path '{path}'")
        return True, False, user
    
    logger.info(f"Authentication successful: user '{username}' ({user['role']}) performing '{action}' on '{path}' from IP {ip}")
    return True, True, user

@app.route('/mediamtx/auth', methods=['POST'])
def mediamtx_auth():
    """
    MediaMTX external authentication endpoint.
    
    MediaMTX sends authentication requests to this endpoint with form data:
    - user: Username
    - pass: Password
    - ip: Client IP address
    - action: Requested action (read, publish, api, metrics, playback)
    - path: MediaMTX path being accessed
    - protocol: Protocol being used (rtsp, rtmp, hls, webrtc, etc.)
    - id: Connection ID
    - query: Query parameters
    """
    try:
        # Get authentication data from MediaMTX
        username = request.form.get('user', '')
        password = request.form.get('pass', '')
        ip = request.form.get('ip', '')
        action = request.form.get('action', '')
        path = request.form.get('path', '')
        protocol = request.form.get('protocol', '')
        connection_id = request.form.get('id', '')
        query = request.form.get('query', '')
        
        logger.info(f"Auth request: user='{username}', action='{action}', path='{path}', protocol='{protocol}', ip='{ip}'")
        
        # Authenticate user and check permissions
        is_authenticated, has_permission, user_info = authenticate_user(username, password, ip, action, path)
        
        if not is_authenticated:
            return "Unauthorized", 401
        
        if not has_permission:
            return "Forbidden", 403
        
        # Authentication and authorization successful
        logger.info(f"Access granted: {username} ({user_info['role']}) -> {action} on {path}")
        return "OK", 200
        
    except Exception as e:
        logger.error(f"Error in authentication endpoint: {e}")
        return "Internal Server Error", 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy", 
        "service": "mediamtx-external-auth",
        "timestamp": datetime.now().isoformat(),
        "users_count": len(USERS)
    })

@app.route('/users', methods=['GET'])
def list_users():
    """List available users (for debugging)."""
    user_list = []
    for username, user_data in USERS.items():
        user_list.append({
            "username": username,
            "role": user_data["role"],
            "permissions": user_data["permissions"]
        })
    return jsonify({"users": user_list})

@app.route('/test-auth', methods=['POST'])
def test_auth():
    """Test authentication endpoint for debugging."""
    data = request.get_json()
    username = data.get('username', '')
    password = data.get('password', '')
    action = data.get('action', 'read')
    path = data.get('path', 'camera1')
    ip = request.remote_addr
    
    is_authenticated, has_permission, user_info = authenticate_user(username, password, ip, action, path)
    
    return jsonify({
        "authenticated": is_authenticated,
        "has_permission": has_permission,
        "user_info": user_info,
        "requested_action": action,
        "requested_path": path
    })

if __name__ == '__main__':
    print("🔐 MediaMTX External Authentication Backend")
    print("=" * 50)
    print("This backend handles authentication for MediaMTX external auth.")
    print("Update mediamtx.yml to use: authHTTPAddress: http://your-backend:8000/mediamtx/auth")
    print("\n📋 Available users:")
    for username, user_data in USERS.items():
        print(f"  {username}: {user_data['password']} (role: {user_data['role']}, permissions: {', '.join(user_data['permissions'])})")
    print("\n🌐 Endpoints:")
    print("  - POST /mediamtx/auth - Main authentication endpoint")
    print("  - GET /health - Health check")
    print("  - GET /users - List users")
    print("  - POST /test-auth - Test authentication")
    print("\n🚀 Starting server on http://0.0.0.0:8000")
    print("📡 MediaMTX auth endpoint: http://0.0.0.0:8000/mediamtx/auth")
    
    app.run(host='0.0.0.0', port=8000, debug=True)

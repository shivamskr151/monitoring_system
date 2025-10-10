#!/usr/bin/env python3
"""
Example backend authentication endpoint for MediaMTX external authentication.

This is a reference implementation showing how your backend should handle
MediaMTX authentication requests. Replace the URL in mediamtx.yml with your
actual backend endpoint.

MediaMTX will send POST requests to your auth endpoint with:
- user: username
- pass: password  
- ip: client IP
- action: requested action (read, publish, api, metrics, etc.)
- path: MediaMTX path being accessed

Your backend should respond with:
- 200 OK: Authentication successful
- 401 Unauthorized: Authentication failed
- 403 Forbidden: User authenticated but lacks permission for this action
"""

from flask import Flask, request, jsonify
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Example user database - replace with your actual user management
USERS = {
    "admin": {
        "password": "admin123",  # In production, use hashed passwords
        "permissions": ["read", "publish", "api", "metrics", "playback"],
        "ips": []  # Empty means allow from any IP
    },
    "viewer": {
        "password": "viewer123",
        "permissions": ["read", "playback"],
        "ips": []
    },
    "guest": {
        "password": "guest123", 
        "permissions": ["read"],
        "ips": []
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
        tuple: (is_authenticated, has_permission)
    """
    # Check if user exists
    if username not in USERS:
        logger.warning(f"Authentication failed: user '{username}' not found")
        return False, False
    
    user = USERS[username]
    
    # Check password
    if user["password"] != password:
        logger.warning(f"Authentication failed: invalid password for user '{username}'")
        return False, False
    
    # Check IP restrictions (if any)
    if user["ips"] and ip not in user["ips"]:
        logger.warning(f"Authentication failed: IP {ip} not allowed for user '{username}'")
        return False, False
    
    # Check permissions
    if action not in user["permissions"]:
        logger.warning(f"Permission denied: user '{username}' lacks permission for action '{action}'")
        return True, False
    
    logger.info(f"Authentication successful: user '{username}' performing '{action}' on '{path}'")
    return True, True

@app.route('/mediamtx/auth', methods=['POST'])
def mediamtx_auth():
    """
    MediaMTX external authentication endpoint.
    
    MediaMTX sends authentication requests to this endpoint.
    """
    try:
        # Get authentication data from MediaMTX
        username = request.form.get('user', '')
        password = request.form.get('pass', '')
        ip = request.form.get('ip', '')
        action = request.form.get('action', '')
        path = request.form.get('path', '')
        
        logger.info(f"Auth request: user='{username}', action='{action}', path='{path}', ip='{ip}'")
        
        # Authenticate user and check permissions
        is_authenticated, has_permission = authenticate_user(username, password, ip, action, path)
        
        if not is_authenticated:
            return "Unauthorized", 401
        
        if not has_permission:
            return "Forbidden", 403
        
        # Authentication and authorization successful
        return "OK", 200
        
    except Exception as e:
        logger.error(f"Error in authentication endpoint: {e}")
        return "Internal Server Error", 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "mediamtx-auth"})

if __name__ == '__main__':
    print("MediaMTX External Authentication Server")
    print("======================================")
    print("This is an example implementation.")
    print("Replace the URL in mediamtx.yml with your actual backend endpoint.")
    print("\nExample users:")
    for username, user_data in USERS.items():
        print(f"  {username}: {user_data['password']} (permissions: {', '.join(user_data['permissions'])})")
    print("\nStarting server on http://localhost:8000")
    print("MediaMTX auth endpoint: http://localhost:8000/mediamtx/auth")
    
    app.run(host='0.0.0.0', port=8000, debug=True)

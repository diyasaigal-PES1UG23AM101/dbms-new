from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import uuid
import os

app = Flask(__name__)
CORS(app)

# ==================== DATA MODELS (In-Memory Databases) ====================

# ASSET_DB (ITM-F-001) - Includes department field for analytics
ASSET_DB = [
    {
        "assetId": "AST-001",
        "assetType": "Laptop",
        "assignedUser": "Alice Johnson",
        "purchaseDate": "2023-01-15",
        "warrantyExpiryDate": "2026-01-15",
        "status": "Active",
        "department": "Engineering"
    },
    {
        "assetId": "AST-002",
        "assetType": "Desktop",
        "assignedUser": "Bob Smith",
        "purchaseDate": "2022-06-20",
        "warrantyExpiryDate": "2025-06-20",
        "status": "Active",
        "department": "Sales"
    },
    {
        "assetId": "AST-003",
        "assetType": "Monitor",
        "assignedUser": "Alice Johnson",
        "purchaseDate": "2023-03-10",
        "warrantyExpiryDate": "2026-03-10",
        "status": "Active",
        "department": "Engineering"
    },
    {
        "assetId": "AST-004",
        "assetType": "Laptop",
        "assignedUser": "Charlie Brown",
        "purchaseDate": "2024-01-05",
        "warrantyExpiryDate": "2027-01-05",
        "status": "Active",
        "department": "Marketing"
    },
    {
        "assetId": "AST-005",
        "assetType": "Server",
        "assignedUser": "IT Department",
        "purchaseDate": "2021-11-12",
        "warrantyExpiryDate": "2024-11-12",
        "status": "Maintenance",
        "department": "IT"
    },
    {
        "assetId": "AST-006",
        "assetType": "Laptop",
        "assignedUser": "David Wilson",
        "purchaseDate": "2023-08-20",
        "warrantyExpiryDate": "2026-08-20",
        "status": "Active",
        "department": "HR"
    },
    {
        "assetId": "AST-007",
        "assetType": "Desktop",
        "assignedUser": "Eva Martinez",
        "purchaseDate": "2022-12-05",
        "warrantyExpiryDate": "2025-12-05",
        "status": "Active",
        "department": "Finance"
    }
]

# LICENSE_DB (ITM-F-010, F-012) - Includes complianceStatus, one entry flagged as 'Unauthorized'
LICENSE_DB = [
    {
        "licenseId": "LIC-001",
        "softwareName": "Microsoft Office 365",
        "licenseKey": "XXXXX-XXXXX-XXXXX-001",
        "totalSeats": 50,
        "usedSeats": 45,
        "expiryDate": "2024-12-31",
        "complianceStatus": "Compliant"
    },
    {
        "licenseId": "LIC-002",
        "softwareName": "Adobe Creative Suite",
        "licenseKey": "XXXXX-XXXXX-XXXXX-002",
        "totalSeats": 20,
        "usedSeats": 18,
        "expiryDate": (datetime.now() + timedelta(days=45)).strftime("%Y-%m-%d"),
        "complianceStatus": "Compliant"
    },
    {
        "licenseId": "LIC-003",
        "softwareName": "Windows Server License",
        "licenseKey": "XXXXX-XXXXX-XXXXX-003",
        "totalSeats": 10,
        "usedSeats": 8,
        "expiryDate": (datetime.now() + timedelta(days=75)).strftime("%Y-%m-%d"),
        "complianceStatus": "Compliant"
    },
    {
        "licenseId": "LIC-004",
        "softwareName": "VMware vSphere",
        "licenseKey": "XXXXX-XXXXX-XXXXX-004",
        "totalSeats": 5,
        "usedSeats": 5,
        "expiryDate": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "complianceStatus": "Unauthorized"
    },
    {
        "licenseId": "LIC-005",
        "softwareName": "Autodesk AutoCAD",
        "licenseKey": "XXXXX-XXXXX-XXXXX-005",
        "totalSeats": 15,
        "usedSeats": 12,
        "expiryDate": "2025-06-30",
        "complianceStatus": "Compliant"
    }
]

# HEALTH_DB (ITM-F-020) - At least 2 entries must breach threshold (cpuLoad > 85% or isOverheating: True)
HEALTH_DB = [
    {
        "deviceId": "DEV-001",
        "cpuLoad": 92,
        "memoryUtil": 78,
        "isOverheating": True,
        "lastCheck": (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "deviceId": "DEV-002",
        "cpuLoad": 45,
        "memoryUtil": 60,
        "isOverheating": False,
        "lastCheck": (datetime.now() - timedelta(minutes=3)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "deviceId": "DEV-003",
        "cpuLoad": 35,
        "memoryUtil": 50,
        "isOverheating": False,
        "lastCheck": (datetime.now() - timedelta(minutes=2)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "deviceId": "DEV-004",
        "cpuLoad": 88,
        "memoryUtil": 85,
        "isOverheating": False,
        "lastCheck": (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "deviceId": "DEV-005",
        "cpuLoad": 25,
        "memoryUtil": 40,
        "isOverheating": False,
        "lastCheck": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    },
    {
        "deviceId": "DEV-006",
        "cpuLoad": 91,
        "memoryUtil": 82,
        "isOverheating": True,
        "lastCheck": (datetime.now() - timedelta(minutes=4)).strftime("%Y-%m-%d %H:%M:%S")
    }
]

# BACKUP_DB (ITM-F-040) - At least 2 entries must be 'Failure' or 'Missed'
BACKUP_DB = [
    {
        "jobId": "BK-001",
        "assetId": "AST-001",
        "lastRunDate": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Success",
        "alertReason": None
    },
    {
        "jobId": "BK-002",
        "assetId": "AST-002",
        "lastRunDate": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Failure",
        "alertReason": "Disk space insufficient"
    },
    {
        "jobId": "BK-003",
        "assetId": "AST-003",
        "lastRunDate": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Success",
        "alertReason": None
    },
    {
        "jobId": "BK-004",
        "assetId": "AST-004",
        "lastRunDate": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Missed",
        "alertReason": "Scheduled time conflict"
    },
    {
        "jobId": "BK-005",
        "assetId": "AST-005",
        "lastRunDate": (datetime.now() - timedelta(hours=12)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Success",
        "alertReason": None
    },
    {
        "jobId": "BK-006",
        "assetId": "AST-006",
        "lastRunDate": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Failure",
        "alertReason": "Network timeout"
    }
]

# NETWORK_DB (ITM-F-030) - At least 2 entries must be flagged (isDowntime: True or abnormalTraffic: True)
NETWORK_DB = [
    {
        "deviceId": "NET-001",
        "bandwidthMB": 450,
        "isDowntime": False,
        "abnormalTraffic": True
    },
    {
        "deviceId": "NET-002",
        "bandwidthMB": 120,
        "isDowntime": False,
        "abnormalTraffic": False
    },
    {
        "deviceId": "NET-003",
        "bandwidthMB": 0,
        "isDowntime": True,
        "abnormalTraffic": False
    },
    {
        "deviceId": "NET-004",
        "bandwidthMB": 280,
        "isDowntime": False,
        "abnormalTraffic": False
    },
    {
        "deviceId": "NET-005",
        "bandwidthMB": 350,
        "isDowntime": False,
        "abnormalTraffic": False
    },
    {
        "deviceId": "NET-006",
        "bandwidthMB": 520,
        "isDowntime": False,
        "abnormalTraffic": True
    }
]

# AUDIT_LOG_DB (ITM-SR-004)
AUDIT_LOG_DB = []

# External Integration Status (ITM-F-041)
INTEGRATION_STATUS = {
    "licenseVendorAPI": {"name": "License Vendor API", "status": "Active", "lastCheck": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    "networkSNMPAgent": {"name": "Network SNMP Agent", "status": "Active", "lastCheck": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    "backupToolX": {"name": "Backup Tool X", "status": "Inactive", "lastCheck": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M:%S")},
    "monitoringService": {"name": "Monitoring Service", "status": "Active", "lastCheck": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
}

# Mock user database for authentication
USER_DB = {
    "admin": {"password": "admin123", "role": "Admin", "name": "Administrator"},
    "itstaff": {"password": "it123", "role": "IT Staff", "name": "IT Staff User"},
    "employee": {"password": "emp123", "role": "Employee", "name": "Alice Johnson"}
}

# Current user session
current_role = None
current_user = None
is_authenticated = False

# ==================== HELPER FUNCTIONS ====================

def add_audit_log(action, details, user_role):
    """Add entry to audit log"""
    log_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "userRole": user_role,
        "action": action,
        "details": details
    }
    AUDIT_LOG_DB.append(log_entry)
    return log_entry

def can_perform_crud(role):
    """Check if role can perform CRUD operations"""
    return role in ["Admin", "IT Staff"]

def calculate_dashboard_metrics():
    """Calculate dashboard metrics from all databases"""
    total_assets = len(ASSET_DB)
    
    # Licenses expiring in next 90 days
    today = datetime.now().date()
    expiry_threshold = today + timedelta(days=90)
    licenses_expiring_soon = sum(
        1 for lic in LICENSE_DB 
        if datetime.strptime(lic["expiryDate"], "%Y-%m-%d").date() <= expiry_threshold
    )
    
    # Hardware health alerts (CPU > 85% or overheating)
    hardware_alerts = sum(
        1 for dev in HEALTH_DB 
        if dev["cpuLoad"] > 85 or dev["isOverheating"]
    )
    
    # Backup failures
    backup_failures = sum(
        1 for job in BACKUP_DB 
        if job["status"] in ["Failure", "Missed"]
    )
    
    # Network events
    network_events = sum(
        1 for net in NETWORK_DB 
        if net["isDowntime"] or net["abnormalTraffic"]
    )
    
    return {
        "totalAssets": total_assets,
        "licensesExpiringSoon": licenses_expiring_soon,
        "hardwareHealthAlerts": hardware_alerts,
        "backupFailures": backup_failures,
        "networkEvents": network_events
    }

# ==================== API ENDPOINTS ====================

@app.route('/api/role', methods=['GET', 'POST'])
def role():
    """Get or set current user role"""
    global current_role
    if request.method == 'POST':
        data = request.json
        current_role = data.get('role', 'Admin')
        return jsonify({"role": current_role})
    return jsonify({"role": current_role})

@app.route('/api/dashboard/metrics', methods=['GET'])
def dashboard_metrics():
    """Get dashboard metrics"""
    return jsonify(calculate_dashboard_metrics())

@app.route('/api/assets', methods=['GET', 'POST'])
def assets():
    """CRUD operations for assets"""
    global current_role
    
    if request.method == 'GET':
        # Filter by assignedUser if Employee role
        if current_role == "Employee":
            filtered_assets = [a for a in ASSET_DB if a["assignedUser"] == "Alice Johnson"]
            return jsonify(filtered_assets)
        return jsonify(ASSET_DB)
    
    elif request.method == 'POST':
        if not can_perform_crud(current_role):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        data = request.json
        action = data.get('action')
        
        if action == 'create':
            new_asset = {
                "assetId": data.get('assetId', f"AST-{str(uuid.uuid4())[:8]}"),
                "assetType": data.get('assetType'),
                "assignedUser": data.get('assignedUser'),
                "purchaseDate": data.get('purchaseDate'),
                "warrantyExpiryDate": data.get('warrantyExpiryDate'),
                "status": data.get('status', 'Active'),
                "department": data.get('department', 'IT')
            }
            ASSET_DB.append(new_asset)
            add_audit_log("CREATE", f"Created asset {new_asset['assetId']}", current_role)
            return jsonify(new_asset), 201
        
        elif action == 'update':
            asset_id = data.get('assetId')
            for i, asset in enumerate(ASSET_DB):
                if asset["assetId"] == asset_id:
                    ASSET_DB[i].update({
                        "assetType": data.get('assetType', asset["assetType"]),
                        "assignedUser": data.get('assignedUser', asset["assignedUser"]),
                        "purchaseDate": data.get('purchaseDate', asset["purchaseDate"]),
                        "warrantyExpiryDate": data.get('warrantyExpiryDate', asset["warrantyExpiryDate"]),
                        "status": data.get('status', asset["status"]),
                        "department": data.get('department', asset.get("department", "IT"))
                    })
                    add_audit_log("UPDATE", f"Updated asset {asset_id}", current_role)
                    return jsonify(ASSET_DB[i])
            return jsonify({"error": "Asset not found"}), 404
        
        elif action == 'delete':
            asset_id = data.get('assetId')
            for i, asset in enumerate(ASSET_DB):
                if asset["assetId"] == asset_id:
                    deleted = ASSET_DB.pop(i)
                    add_audit_log("DELETE", f"Deleted asset {asset_id}", current_role)
                    return jsonify(deleted)
            return jsonify({"error": "Asset not found"}), 404

@app.route('/api/licenses', methods=['GET', 'POST'])
def licenses():
    """CRUD operations for licenses"""
    global current_role
    
    if request.method == 'GET':
        return jsonify(LICENSE_DB)
    
    elif request.method == 'POST':
        if not can_perform_crud(current_role):
            return jsonify({"error": "Insufficient permissions"}), 403
        
        data = request.json
        action = data.get('action')
        
        if action == 'create':
            new_license = {
                "licenseId": data.get('licenseId', f"LIC-{str(uuid.uuid4())[:8]}"),
                "softwareName": data.get('softwareName'),
                "licenseKey": data.get('licenseKey'),
                "totalSeats": data.get('totalSeats'),
                "usedSeats": data.get('usedSeats', 0),
                "expiryDate": data.get('expiryDate'),
                "complianceStatus": data.get('complianceStatus', 'Compliant')
            }
            LICENSE_DB.append(new_license)
            add_audit_log("CREATE", f"Created license {new_license['licenseId']}", current_role)
            return jsonify(new_license), 201
        
        elif action == 'update':
            license_id = data.get('licenseId')
            for i, lic in enumerate(LICENSE_DB):
                if lic["licenseId"] == license_id:
                    LICENSE_DB[i].update({
                        "softwareName": data.get('softwareName', lic["softwareName"]),
                        "licenseKey": data.get('licenseKey', lic["licenseKey"]),
                        "totalSeats": data.get('totalSeats', lic["totalSeats"]),
                        "usedSeats": data.get('usedSeats', lic["usedSeats"]),
                        "expiryDate": data.get('expiryDate', lic["expiryDate"]),
                        "complianceStatus": data.get('complianceStatus', lic.get("complianceStatus", "Compliant"))
                    })
                    add_audit_log("UPDATE", f"Updated license {license_id}", current_role)
                    return jsonify(LICENSE_DB[i])
            return jsonify({"error": "License not found"}), 404
        
        elif action == 'delete':
            license_id = data.get('licenseId')
            for i, lic in enumerate(LICENSE_DB):
                if lic["licenseId"] == license_id:
                    deleted = LICENSE_DB.pop(i)
                    add_audit_log("DELETE", f"Deleted license {license_id}", current_role)
                    return jsonify(deleted)
            return jsonify({"error": "License not found"}), 404

@app.route('/api/monitoring/hardware', methods=['GET'])
def hardware_health():
    """Get hardware health monitoring data"""
    return jsonify(HEALTH_DB)

@app.route('/api/monitoring/network', methods=['GET'])
def network_usage():
    """Get network usage monitoring data"""
    return jsonify(NETWORK_DB)

@app.route('/api/monitoring/backup', methods=['GET'])
def backup_recovery():
    """Get backup and recovery monitoring data"""
    return jsonify(BACKUP_DB)

@app.route('/api/audit-log', methods=['GET'])
def audit_log():
    """Get audit log (Admin/IT Staff only)"""
    global current_role
    if current_role not in ["Admin", "IT Staff"]:
        return jsonify({"error": "Insufficient permissions"}), 403
    return jsonify(AUDIT_LOG_DB)

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User authentication endpoint (ITM-SR-002) with MFA for Admin"""
    global current_role, current_user, is_authenticated
    data = request.json
    username = data.get('username', '').lower()
    password = data.get('password', '')
    mfa_code = data.get('mfaCode', '')
    use_biometric = data.get('useBiometric', False)
    
    # Mock biometric authentication (non-functional as per requirements)
    if use_biometric:
        return jsonify({
            "success": False,
            "message": "Biometric authentication is not yet implemented. Please use password login."
        }), 400
    
    # Check credentials
    if username in USER_DB and USER_DB[username]["password"] == password:
        # Admin requires MFA (mock code: '123456')
        if USER_DB[username]["role"] == "Admin":
            if not mfa_code or mfa_code != '123456':
                return jsonify({
                    "success": False,
                    "requiresMFA": True,
                    "message": "MFA code required for Admin login. Use code: 123456"
                }), 401
        
        current_user = username
        current_role = USER_DB[username]["role"]
        is_authenticated = True
        add_audit_log("LOGIN", f"User {username} logged in", current_role)
        return jsonify({
            "success": True,
            "role": current_role,
            "name": USER_DB[username]["name"]
        })
    else:
        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    """User logout endpoint"""
    global current_user, current_role, is_authenticated
    if current_user:
        add_audit_log("LOGOUT", f"User {current_user} logged out", current_role)
    current_user = None
    current_role = None
    is_authenticated = False
    return jsonify({"success": True})

@app.route('/api/auth/status', methods=['GET'])
def auth_status():
    """Get current authentication status"""
    global current_role, current_user, is_authenticated
    return jsonify({
        "authenticated": is_authenticated,
        "role": current_role,
        "user": current_user
    })

@app.route('/api/monitoring/backup/verify', methods=['POST'])
def backup_verify():
    """Automated backup verification endpoint (ITM-F-041) - Resets status to 'Under Investigation'"""
    global current_role, is_authenticated
    if not is_authenticated or current_role not in ["Admin", "IT Staff"]:
        return jsonify({"error": "Insufficient permissions"}), 403
    
    # Find failed/missed backup jobs
    failed_jobs = [job for job in BACKUP_DB if job["status"] in ["Failure", "Missed"]]
    
    # Simulate verification process and reset status to 'Under Investigation'
    verification_results = []
    for job in failed_jobs:
        # Update job status to 'Under Investigation'
        for i, backup_job in enumerate(BACKUP_DB):
            if backup_job["jobId"] == job["jobId"]:
                BACKUP_DB[i]["status"] = "Under Investigation"
                break
        
        verification_results.append({
            "jobId": job["jobId"],
            "assetId": job["assetId"],
            "previousStatus": job["status"],
            "newStatus": "Under Investigation",
            "alertReason": job["alertReason"],
            "verificationStatus": "Under Investigation",
            "recommendedAction": "Review backup configuration and retry backup job"
        })
    
    add_audit_log("VERIFY", f"Backup verification run - {len(failed_jobs)} jobs set to 'Under Investigation'", current_role)
    
    return jsonify({
        "verifiedJobs": len(failed_jobs),
        "results": verification_results,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

@app.route('/api/integrations/status', methods=['GET'])
def integration_status():
    """Get external integration status"""
    return jsonify(INTEGRATION_STATUS)

@app.route('/api/analytics/assets-by-department', methods=['GET'])
def assets_by_department():
    """Get asset distribution by department for analytics (ITM-F-061)"""
    department_counts = {}
    for asset in ASSET_DB:
        dept = asset.get("department", "Unknown")
        department_counts[dept] = department_counts.get(dept, 0) + 1
    
    return jsonify(department_counts)

@app.route('/api/assets/<asset_id>/qr', methods=['GET'])
def generate_qr(asset_id):
    """Generate QR code data for asset (ITM-F-001)"""
    asset = next((a for a in ASSET_DB if a["assetId"] == asset_id), None)
    if not asset:
        return jsonify({"error": "Asset not found"}), 404
    
    # Generate mock QR code data
    qr_data = {
        "assetId": asset_id,
        "assetType": asset["assetType"],
        "url": f"http://localhost:5000/assets/{asset_id}",
        "message": "In a real application, scanning this QR code would link to the asset's details page."
    }
    
    user_role = current_role if current_role else "System"
    add_audit_log("QR_GENERATE", f"QR code generated for asset {asset_id}", user_role)
    return jsonify(qr_data)

@app.route('/')
def index():
    """Serve the main HTML file"""
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), 'index.html')

if __name__ == '__main__':
    # Initialize audit log with startup entry
    add_audit_log("SYSTEM", "IIMS System Started", "System")
    app.run(debug=True, port=5000)


import unittest
import json
from server import app, ASSET_DB, LICENSE_DB

class IIMSExtendedTestCase(unittest.TestCase):
    """Extended test cases to increase code coverage"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        # Reset authentication state
        import server
        server.current_role = None
        server.current_user = None
        server.is_authenticated = False
    
    def test_login_itstaff(self):
        """Test IT Staff login (no MFA required)"""
        response = self.app.post('/api/auth/login',
                                json={'username': 'itstaff', 'password': 'it123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success', False))
        self.assertEqual(data.get('role'), 'IT Staff')
    
    def test_login_employee(self):
        """Test Employee login"""
        response = self.app.post('/api/auth/login',
                                json={'username': 'employee', 'password': 'emp123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success', False))
        self.assertEqual(data.get('role'), 'Employee')
    
    def test_logout(self):
        """Test logout functionality"""
        # First login
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Then logout
        response = self.app.post('/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success', False))
    
    def test_auth_status_authenticated(self):
        """Test auth status when authenticated"""
        # Login first
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Check status
        response = self.app.get('/api/auth/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('authenticated', False))
        self.assertEqual(data.get('role'), 'IT Staff')
    
    def test_create_asset_authenticated(self):
        """Test creating asset with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Create asset
        response = self.app.post('/api/assets',
                                json={
                                    'action': 'create',
                                    'assetId': 'TEST-NEW-001',
                                    'assetType': 'Test Device',
                                    'assignedUser': 'Test User',
                                    'purchaseDate': '2024-01-01',
                                    'warrantyExpiryDate': '2027-01-01',
                                    'department': 'IT',
                                    'status': 'Active'
                                })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['assetId'], 'TEST-NEW-001')
    
    def test_update_asset_authenticated(self):
        """Test updating asset with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Update existing asset
        if len(ASSET_DB) > 0:
            asset_id = ASSET_DB[0]['assetId']
            response = self.app.post('/api/assets',
                                    json={
                                        'action': 'update',
                                        'assetId': asset_id,
                                        'assetType': 'Updated Type',
                                        'assignedUser': ASSET_DB[0]['assignedUser'],
                                        'purchaseDate': ASSET_DB[0]['purchaseDate'],
                                        'warrantyExpiryDate': ASSET_DB[0]['warrantyExpiryDate'],
                                        'department': ASSET_DB[0]['department'],
                                        'status': 'Maintenance'
                                    })
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['status'], 'Maintenance')
    
    def test_delete_asset_authenticated(self):
        """Test deleting asset with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Create a test asset first
        self.app.post('/api/assets',
                     json={
                         'action': 'create',
                         'assetId': 'TEST-DELETE-001',
                         'assetType': 'Test Device',
                         'assignedUser': 'Test User',
                         'purchaseDate': '2024-01-01',
                         'warrantyExpiryDate': '2027-01-01',
                         'department': 'IT',
                         'status': 'Active'
                     })
        # Delete it
        response = self.app.post('/api/assets',
                                json={'action': 'delete', 'assetId': 'TEST-DELETE-001'})
        self.assertEqual(response.status_code, 200)
    
    def test_create_license_authenticated(self):
        """Test creating license with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Create license
        response = self.app.post('/api/licenses',
                                json={
                                    'action': 'create',
                                    'licenseId': 'TEST-LIC-001',
                                    'softwareName': 'Test Software',
                                    'licenseKey': 'TEST-KEY-001',
                                    'totalSeats': 10,
                                    'usedSeats': 5,
                                    'expiryDate': '2025-12-31',
                                    'complianceStatus': 'Compliant'
                                })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['licenseId'], 'TEST-LIC-001')
    
    def test_update_license_authenticated(self):
        """Test updating license with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Update existing license
        if len(LICENSE_DB) > 0:
            license_id = LICENSE_DB[0]['licenseId']
            response = self.app.post('/api/licenses',
                                    json={
                                        'action': 'update',
                                        'licenseId': license_id,
                                        'softwareName': LICENSE_DB[0]['softwareName'],
                                        'licenseKey': LICENSE_DB[0]['licenseKey'],
                                        'totalSeats': LICENSE_DB[0]['totalSeats'],
                                        'usedSeats': 50,
                                        'expiryDate': LICENSE_DB[0]['expiryDate'],
                                        'complianceStatus': 'Compliant'
                                    })
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['usedSeats'], 50)
    
    def test_delete_license_authenticated(self):
        """Test deleting license with authentication"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Create a test license first
        self.app.post('/api/licenses',
                     json={
                         'action': 'create',
                         'licenseId': 'TEST-DEL-LIC-001',
                         'softwareName': 'Test Software',
                         'licenseKey': 'TEST-KEY',
                         'totalSeats': 10,
                         'usedSeats': 5,
                         'expiryDate': '2025-12-31',
                         'complianceStatus': 'Compliant'
                     })
        # Delete it
        response = self.app.post('/api/licenses',
                                json={'action': 'delete', 'licenseId': 'TEST-DEL-LIC-001'})
        self.assertEqual(response.status_code, 200)
    
    def test_backup_verification_authenticated(self):
        """Test backup verification with proper authentication"""
        # Login as Admin
        self.app.post('/api/auth/login',
                     json={'username': 'admin', 'password': 'admin123', 'mfaCode': '123456'})
        # Run verification
        response = self.app.post('/api/monitoring/backup/verify')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('verifiedJobs', data)
        self.assertIn('results', data)
    
    def test_employee_asset_filtering(self):
        """Test that Employee role only sees assigned assets"""
        # Login as Employee
        self.app.post('/api/auth/login',
                     json={'username': 'employee', 'password': 'emp123'})
        # Get assets
        response = self.app.get('/api/assets')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # All assets should be assigned to Alice Johnson
        for asset in data:
            self.assertEqual(asset['assignedUser'], 'Alice Johnson')
    
    def test_audit_log_access(self):
        """Test audit log access for Admin/IT Staff"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Access audit log
        response = self.app.get('/api/audit-log')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_audit_log_employee_denied(self):
        """Test that Employee cannot access audit log"""
        # Login as Employee
        self.app.post('/api/auth/login',
                     json={'username': 'employee', 'password': 'emp123'})
        # Try to access audit log
        response = self.app.get('/api/audit-log')
        self.assertEqual(response.status_code, 403)
    
    def test_asset_not_found_update(self):
        """Test updating non-existent asset"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Try to update non-existent asset
        response = self.app.post('/api/assets',
                                json={
                                    'action': 'update',
                                    'assetId': 'NON-EXISTENT-001',
                                    'assetType': 'Test'
                                })
        self.assertEqual(response.status_code, 404)
    
    def test_license_not_found_update(self):
        """Test updating non-existent license"""
        # Login as IT Staff
        self.app.post('/api/auth/login',
                     json={'username': 'itstaff', 'password': 'it123'})
        # Try to update non-existent license
        response = self.app.post('/api/licenses',
                                json={
                                    'action': 'update',
                                    'licenseId': 'NON-EXISTENT-001',
                                    'softwareName': 'Test'
                                })
        self.assertEqual(response.status_code, 404)
    
    def test_qr_code_invalid_asset(self):
        """Test QR code generation for non-existent asset"""
        response = self.app.get('/api/assets/INVALID-ASSET-001/qr')
        self.assertEqual(response.status_code, 404)
    
    def test_biometric_login_mock(self):
        """Test biometric login mock (should fail)"""
        response = self.app.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123', 'useBiometric': True})
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data.get('success', True))

if __name__ == '__main__':
    unittest.main()


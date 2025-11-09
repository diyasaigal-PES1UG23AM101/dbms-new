import unittest
import json
from server import app

class IIMSIntegrationTestCase(unittest.TestCase):
    """Integration tests for IIMS application"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
        # Reset authentication state before each test
        import server
        server.current_role = None
        server.current_user = None
        server.is_authenticated = False
    
    def test_full_workflow(self):
        """Test complete workflow: login -> get data -> logout"""
        # 1. Check auth status (should be unauthenticated)
        response = self.app.get('/api/auth/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data.get('authenticated', True))
        
        # 2. Login as IT Staff (no MFA required)
        response = self.app.post('/api/auth/login',
                                json={'username': 'itstaff', 'password': 'it123'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success', False))
        
        # 3. Check auth status (should be authenticated)
        response = self.app.get('/api/auth/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('authenticated', False))
        
        # 4. Get dashboard metrics
        response = self.app.get('/api/dashboard/metrics')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('totalAssets', data)
        
        # 5. Logout
        response = self.app.post('/api/auth/logout')
        self.assertEqual(response.status_code, 200)
        
        # 6. Verify logout
        response = self.app.get('/api/auth/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data.get('authenticated', True))
    
    def test_admin_mfa_workflow(self):
        """Test admin login with MFA workflow"""
        # 1. Try login without MFA (should fail)
        response = self.app.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123'})
        self.assertEqual(response.status_code, 401)
        data = json.loads(response.data)
        self.assertTrue(data.get('requiresMFA', False))
        
        # 2. Login with correct MFA
        response = self.app.post('/api/auth/login',
                                json={'username': 'admin', 'password': 'admin123', 'mfaCode': '123456'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data.get('success', False))
        self.assertEqual(data.get('role'), 'Admin')

if __name__ == '__main__':
    unittest.main()


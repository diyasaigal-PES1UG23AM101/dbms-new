# IT Infrastructure Management System (IIMS)

A comprehensive full-stack application prototype for managing IT infrastructure assets, licenses, monitoring, and operations.

## Features

- **Asset Management**: Full CRUD operations with QR code generation
- **License Management**: Track software licenses with compliance status
- **Monitoring**: Hardware health, network usage, and backup status
- **Role-Based Access Control**: Admin, IT Staff, and Employee roles
- **Authentication**: Login with MFA support for Admin users
- **Analytics**: Asset distribution by department
- **Integration Status**: External service monitoring
- **Audit Logging**: Complete activity tracking

## Technology Stack

- **Backend**: Python 3.10+ with Flask
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Database**: In-memory data structures (prototype)
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python server.py
   ```

3. **Access the application:**
   Open `http://localhost:5000` in your browser

### Docker Deployment

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up -d
   ```

2. **Or build and run with Docker:**
   ```bash
   docker build -t iims .
   docker run -p 5000:5000 iims
   ```

## Login Credentials

- **Admin**: `admin` / `admin123` (MFA: `123456`)
- **IT Staff**: `itstaff` / `it123`
- **Employee**: `employee` / `emp123`

## Testing

Run the test suite:

```bash
pytest tests/ -v
```

With coverage:

```bash
pytest tests/ -v --cov=server --cov-report=html
```

## CI/CD Pipeline

The project includes a GitHub Actions CI/CD pipeline that:

1. **Runs tests** on every push/PR
2. **Lints code** for quality checks
3. **Builds Docker image** on successful tests
4. **Scans for security** vulnerabilities
5. **Deploys** to production (on main/master branch)

### Pipeline Jobs

- `test`: Runs unit and integration tests
- `lint`: Code quality checks (flake8, black)
- `build-docker`: Builds Docker image
- `security-scan`: Security vulnerability scanning
- `deploy`: Automated deployment (production only)

## Project Structure

```
.
├── server.py              # Flask backend application
├── index.html             # Frontend single-page application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container configuration
├── docker-compose.yml     # Docker Compose configuration
├── pytest.ini            # Pytest configuration
├── tests/                 # Test suite
│   ├── test_server.py    # Unit tests
│   └── test_integration.py # Integration tests
└── .github/
    └── workflows/
        └── ci-cd.yml     # CI/CD pipeline configuration
```

## Development

### Adding New Features

1. Create feature branch
2. Implement feature with tests
3. Ensure all tests pass
4. Submit pull request
5. CI/CD pipeline validates changes

### Code Quality

- Follow PEP 8 style guide
- Write tests for new features
- Maintain test coverage > 80%
- Run linters before committing

## Deployment

### Manual Deployment

1. Build Docker image: `docker build -t iims .`
2. Run container: `docker run -p 5000:5000 iims`

### Automated Deployment

The CI/CD pipeline automatically deploys to production when:
- Code is pushed to `main` or `master` branch
- All tests pass
- Docker image builds successfully

## Security

- Non-root user in Docker container
- Health checks enabled
- Security scanning in CI/CD
- MFA for admin accounts
- Audit logging for all operations

## License

This is a prototype/demo application for educational purposes.

## Support

For issues or questions, please open an issue in the repository.


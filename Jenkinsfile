pipeline {

    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        SERVICE_ID = 'fastapi-erp'
        SERVICE_NAME = 'FastAPI ERP'
        SERVICE_DESCRIPTION = 'FastAPI ERP Application'

        DEPLOY_DIR = 'D:\\apps\\fastapi-erp'

        PORT = '7785'
        VAULT_PATH = '/global'
    }

    stages {

        stage('Check Environment') {
            steps {
                bat '''
                    SET PATH=%PYTHON_HOME%;%PYTHON_HOME%\\Scripts;%PATH%

                    echo ==========================================
                    echo PYTHON
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" --version
                    "%PYTHON_HOME%\\python.exe" -m pip --version

                    echo ==========================================
                    echo GIT
                    echo ==========================================

                    git --version
                '''
            }
        }

        stage('Stop Service') {
            steps {
                bat '''
                    "%PYTHON_HOME%\\python.exe" ^
                        "%SERVICE_MANAGER%" ^
                        stop ^
                        "%SERVICE_ID%"

                    exit /B 0
                '''
            }
        }

        stage('Deploy Files') {
            steps {
                powershell '''
                    $source = $env:WORKSPACE
                    $destination = $env:DEPLOY_DIR

                    if (-not (Test-Path $destination)) {
                        New-Item `
                            -ItemType Directory `
                            -Path $destination `
                            -Force | Out-Null
                    }

                    robocopy `
                        $source `
                        $destination `
                        /MIR `
                        /XD ".git" ".venv" "__pycache__" ".pytest_cache" `
                        /XF ".env" "*.pyc"

                    $code = $LASTEXITCODE

                    # Robocopy 0-7 = OK
                    if ($code -gt 7) {
                        throw "Robocopy failed with exit code $code"
                    }

                    exit 0
                '''
            }
        }


        // ============================================================
        // 4. Preparar entorno Python
        // ============================================================

        stage('Prepare Python Environment') {
            steps {
                bat '''
                    echo ==========================================
                    echo Preparing Python virtual environment
                    echo ==========================================

                    if not exist "%DEPLOY_DIR%\\.venv" (
                        "%PYTHON_HOME%\\python.exe" ^
                            -m venv ^
                            "%DEPLOY_DIR%\\.venv"
                    )

                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        -m pip install ^
                        --upgrade pip
                '''
            }
        }

        stage('Install Poetry') {
            steps {
                bat '''
                    "%DEPLOY_DIR%\\.venv\\Scripts\\python.exe" ^
                        -m pip install ^
                        poetry

                    if errorlevel 1 (
                        echo ERROR: Poetry installation failed.
                        exit /B 1
                    )
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    cd /D "%DEPLOY_DIR%"

                    SET POETRY_VIRTUALENVS_CREATE=false

                    "%DEPLOY_DIR%\\.venv\\Scripts\\poetry.exe" ^
                        install ^
                        --only main ^
                        --no-interaction ^
                        --no-ansi

                    if errorlevel 1 (
                        echo ERROR: Poetry install failed.
                        exit /B 1
                    )
                '''
            }
        }

        stage('Configure Service') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'VAULT_TOKEN',
                        variable: 'VAULT_TOKEN'
                    )
                ]) {
                    bat '''
                        echo ==========================================
                        echo Configuring FastAPI ERP Windows service
                        echo ==========================================

                        "%PYTHON_HOME%\\python.exe" "%SERVICE_MANAGER%" install ^
                            "%SERVICE_ID%" ^
                            "%DEPLOY_DIR%" ^
                            --name "%SERVICE_NAME%" ^
                            --description "%SERVICE_DESCRIPTION%" ^
                            --depends-on Vault ^
                            --executable "%DEPLOY_DIR%\\.venv\\Scripts\\uvicorn.exe" ^
                            --args "main:app --host 127.0.0.1 --port %PORT%" ^
                            --env "VAULT_ADDR=%VAULT_ADDR%" ^
                            --env "VAULT_PATH=%VAULT_PATH%" ^
                            --env "VAULT_TOKEN=%VAULT_TOKEN%"

                        if errorlevel 1 (
                            echo ERROR: Service configuration failed.
                            exit /B 1
                        )
                    '''
                }
            }
        }

        stage('Start Service') {
            steps {
                bat '''
                    echo ==========================================
                    echo Starting FastAPI ERP
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" "%SERVICE_MANAGER%" start "%SERVICE_ID%"

                    if errorlevel 1 (
                        echo ERROR: Could not start FastAPI ERP.
                        exit /B 1
                    )
                '''
            }
        }

        stage('Verify Service') {
            steps {
                bat '''
                    echo ==========================================
                    echo Checking Windows service
                    echo ==========================================

                    "%PYTHON_HOME%\\python.exe" ^
                        "%SERVICE_MANAGER%" ^
                        status ^
                        "%SERVICE_ID%"

                    if errorlevel 1 (
                        echo ERROR: FastAPI ERP service is not running.
                        exit /B 1
                    )

                    echo ==========================================
                    echo Checking port %PORT%
                    echo ==========================================

                    netstat -ano | findstr ":%PORT%"

                    if errorlevel 1 (
                        echo ERROR: FastAPI ERP is not listening on port %PORT%.
                        exit /B 1
                    )
                '''
            }
        }

        stage('Health Check') {
            steps {
                powershell '''
                    $url = "http://127.0.0.1:$env:PORT/docs"
                    $maxAttempts = 5
                    for ($attempt = 1; $attempt -le $maxAttempts; $attempt++) {

                        Write-Host "Health check $attempt/$maxAttempts"
                        Write-Host $url

                        try {

                            $response = Invoke-WebRequest `
                                -UseBasicParsing `
                                -Uri $url `
                                -TimeoutSec 5

                            if ($response.StatusCode -eq 200) {

                                Write-Host "FastAPI ERP OK"

                                exit 0
                            }

                            Write-Host "HTTP status: $($response.StatusCode)"
                        }
                        catch {

                            Write-Host "FastAPI ERP aun no disponible."
                            Write-Host $_.Exception.Message
                        }

                        Start-Sleep -Seconds 3
                    }

                    throw "FastAPI ERP no respondio al health check."
                '''
            }
        }
    }


    post {

        success {
            echo '=========================================='
            echo 'FastAPI ERP desplegado correctamente.'
            echo 'Puerto interno: 7785'
            echo 'Base path publico: /fastapi'
            echo 'Nginx debe publicar: https://DOMINIO/fastapi/'
            echo '=========================================='
        }

        failure {
            echo '=========================================='
            echo 'Fallo desplegando FastAPI ERP.'
            echo '=========================================='
        }
    }
}
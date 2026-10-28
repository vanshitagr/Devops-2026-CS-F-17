pipeline {
    agent any

    options {
        disableConcurrentBuilds()
        skipDefaultCheckout(true)
    }

    environment {
        FEEDBACK_FILE       = 'feedback.txt'
        BACKEND_REPORT      = 'backend/test-results.xml'
        FRONTEND_REPORT     = 'frontend/test-results.xml'
        GIT_CREDENTIALS     = 'github-credentials' // Configure this Credential ID in Jenkins
    }

    stages {

        stage('Checkout') {
            steps {
                echo '===> Checking out repository from SCM...'
                checkout scm
            }
        }

        stage('Check Feedback Commit') {
            steps {
                script {
                    def commitMessage = ''
                    def changedFiles = ''

                    if (isUnix()) {
                        commitMessage = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()
                        changedFiles  = sh(script: 'git diff-tree --no-commit-id --name-only -r HEAD', returnStdout: true).trim()
                    } else {
                        commitMessage = bat(script: '@git log -1 --pretty=%%B', returnStdout: true).trim()
                        changedFiles  = bat(script: '@git diff-tree --no-commit-id --name-only -r HEAD', returnStdout: true).trim()
                    }

                    echo "Latest commit message: ${commitMessage}"
                    echo "Changed files: ${changedFiles}"

                    def files = changedFiles
                        .split('\\r?\\n')
                        .collect { it.trim() }
                        .findAll { it }

                    if (
                        commitMessage.contains('[JENKINS-FEEDBACK]') ||
                        (files.size() == 1 && files[0] == 'feedback.txt')
                    ) {
                        env.SKIP_FEEDBACK_PIPELINE = 'true'
                        echo 'Jenkins feedback commit detected.'
                        echo 'Skipping remaining pipeline steps to prevent infinite webhook loops.'
                    } else {
                        env.SKIP_FEEDBACK_PIPELINE = 'false'
                        echo 'Normal developer commit detected. Proceeding with build.'
                    }
                }
            }
        }

        stage('Install Dependencies') {
            when {
                expression {
                    env.SKIP_FEEDBACK_PIPELINE != 'true'
                }
            }

            steps {
                echo '===> Installing Backend dependencies...'
                dir('backend') {
                    script {
                        if (isUnix()) {
                            sh 'npm ci || npm install'
                        } else {
                            bat 'npm ci || npm install'
                        }
                    }
                }

                echo '===> Installing Frontend dependencies...'
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm ci || npm install'
                        } else {
                            bat 'npm ci || npm install'
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            when {
                expression {
                    env.SKIP_FEEDBACK_PIPELINE != 'true'
                }
            }

            steps {
                script {
                    def backendExitCode = 0
                    def frontendExitCode = 0

                    echo '===> Running Backend Unit Tests (generating backend/test-results.xml)...'
                    dir('backend') {
                        if (isUnix()) {
                            backendExitCode = sh(
                                returnStatus: true,
                                script: 'npm run test:ci || npm test -- --test-reporter=junit --test-reporter-destination=test-results.xml'
                            )
                        } else {
                            backendExitCode = bat(
                                returnStatus: true,
                                script: 'npm run test:ci || npm test -- --test-reporter=junit --test-reporter-destination=test-results.xml'
                            )
                        }
                    }

                    echo '===> Running Frontend Unit Tests (generating frontend/test-results.xml)...'
                    dir('frontend') {
                        if (isUnix()) {
                            frontendExitCode = sh(
                                returnStatus: true,
                                script: 'npm run test:ci || npm test -- --test-reporter=junit --test-reporter-destination=test-results.xml'
                            )
                        } else {
                            frontendExitCode = bat(
                                returnStatus: true,
                                script: 'npm run test:ci || npm test -- --test-reporter=junit --test-reporter-destination=test-results.xml'
                            )
                        }
                    }

                    echo "Backend Test Exit Code: ${backendExitCode}"
                    echo "Frontend Test Exit Code: ${frontendExitCode}"

                    if (backendExitCode == 0 && frontendExitCode == 0) {
                        echo 'All backend and frontend tests passed.'
                    } else {
                        echo 'One or more test suites failed. Continuing to generate feedback...'
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }

        stage('Build Frontend Bundle') {
            when {
                expression {
                    env.SKIP_FEEDBACK_PIPELINE != 'true'
                }
            }

            steps {
                echo '===> Building Frontend production bundle with Vite...'
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm run build'
                        } else {
                            bat 'npm run build'
                        }
                    }
                }
            }
        }

        stage('Docker Compose Validation') {
            when {
                expression {
                    env.SKIP_FEEDBACK_PIPELINE != 'true'
                }
            }

            steps {
                echo '===> Validating Docker compose configuration...'
                script {
                    if (isUnix()) {
                        sh 'docker compose config || docker-compose config || true'
                    } else {
                        bat 'docker compose config || docker-compose config || echo Docker validation step completed'
                    }
                }
            }
        }

        stage('Generate Feedback') {
            when {
                expression {
                    env.SKIP_FEEDBACK_PIPELINE != 'true'
                }
            }

            steps {
                script {
                    if (isUnix()) {
                        sh '''
python3 - << 'EOF'
import xml.etree.ElementTree as ET
import os, glob
from datetime import datetime, timezone

report_files = ['backend/test-results.xml', 'frontend/test-results.xml']
total = 0; failed = 0; errors = 0; skipped = 0
test_rows = []

for rf in report_files:
    if os.path.exists(rf):
        try:
            tree = ET.parse(rf)
            root = tree.getroot()
            for tc in root.iter('testcase'):
                total += 1
                name = tc.get('name', 'Unnamed Test')
                status = 'PASS'
                if tc.find('failure') is not None:
                    status = 'FAIL'; failed += 1
                elif tc.find('error') is not None:
                    status = 'ERROR'; errors += 1
                elif tc.find('skipped') is not None:
                    status = 'SKIPPED'; skipped += 1
                test_rows.append(f'{name:<60} : {status}')
        except Exception as e:
            test_rows.append(f'Error reading {rf}: {str(e)}')

passed = total - failed - errors - skipped
overall = 'PASS' if (failed + errors) == 0 and total > 0 else ('FAIL' if total > 0 else 'NO TESTS')
timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
report_text = f"""========================================
DevOps-2026-CS-F-17 - Jenkins Test Feedback
========================================

Build Number : {os.getenv('BUILD_NUMBER', '1')}
Job Name     : {os.getenv('JOB_NAME', 'Devops-2026-CS-F-17')}
Branch       : {os.getenv('GIT_BRANCH', 'main')}
Commit       : {os.getenv('GIT_COMMIT', 'N/A')}
Date         : {timestamp}

TEST SUMMARY
----------------------------------------
Total Tests  : {total}
Passed       : {passed}
Failed       : {failed}
Skipped      : {skipped}
Errors       : {errors}
Overall      : {overall}

TEST CASE RESULTS
----------------------------------------
""" + '\n'.join(test_rows) + """
========================================
"""

with open('feedback.txt', 'a', encoding='utf-8') as f:
    f.write(report_text + '\n')
print(report_text)
EOF
'''
                    } else {
                        powershell '''
                            $reportFiles = @("backend/test-results.xml", "frontend/test-results.xml")

                            $total = 0
                            $failed = 0
                            $errors = 0
                            $skipped = 0
                            $testRows = ""

                            foreach ($file in $reportFiles) {
                                if (Test-Path $file) {
                                    [xml]$report = Get-Content $file
                                    $cases = @($report.SelectNodes("//testcase"))

                                    foreach ($test in $cases) {
                                        $total++
                                        $testName = [string]$test.name

                                        if ([string]::IsNullOrWhiteSpace($testName)) {
                                            $testName = "Unnamed Test"
                                        }

                                        $testStatus = "PASS"

                                        if ($null -ne $test.failure) {
                                            $testStatus = "FAIL"
                                            $failed++
                                        }
                                        elseif ($null -ne $test.error) {
                                            $testStatus = "ERROR"
                                            $errors++
                                        }
                                        elseif ($null -ne $test.skipped) {
                                            $testStatus = "SKIPPED"
                                            $skipped++
                                        }

                                        $testRows += ("{0,-60} : {1}`r`n" -f $testName, $testStatus)
                                    }
                                }
                            }

                            $passed = $total - $failed - $errors - $skipped

                            if (($failed + $errors) -eq 0 -and $total -gt 0) {
                                $status = "PASS"
                            }
                            elseif ($total -eq 0) {
                                $status = "NO TESTS"
                            }
                            else {
                                $status = "FAIL"
                            }

                            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

                            $newFeedback = @"
========================================
DevOps-2026-CS-F-17 - Jenkins Test Feedback
========================================

Build Number : $env:BUILD_NUMBER
Job Name     : $env:JOB_NAME
Branch       : $env:GIT_BRANCH
Commit       : $env:GIT_COMMIT
Date         : $timestamp

TEST SUMMARY
----------------------------------------
Total Tests  : $total
Passed       : $passed
Failed       : $failed
Skipped      : $skipped
Errors       : $errors
Overall      : $status

TEST CASE RESULTS
----------------------------------------
$testRows========================================

"@

                            Add-Content `
                                -Path "feedback.txt" `
                                -Value $newFeedback `
                                -Encoding utf8

                            Write-Host ""
                            Write-Host "========================================"
                            Write-Host "       TEST FEEDBACK SUMMARY"
                            Write-Host "========================================"
                            Write-Host "Total   : $total"
                            Write-Host "Passed  : $passed"
                            Write-Host "Failed  : $failed"
                            Write-Host "Skipped : $skipped"
                            Write-Host "Errors  : $errors"
                            Write-Host "Status  : $status"
                            Write-Host "========================================"
                        '''
                    }
                }
            }
        }

        stage('Push Feedback to Main') {
            when {
                allOf {
                    expression {
                        env.SKIP_FEEDBACK_PIPELINE != 'true'
                    }
                    branch 'main'
                }
            }

            steps {
                script {
                    try {
                        withCredentials([
                            gitUsernamePassword(
                                credentialsId: env.GIT_CREDENTIALS,
                                gitToolName: 'Default'
                            )
                        ]) {
                            if (isUnix()) {
                                sh '''
                                    git config user.name "Jenkins"
                                    git config user.email "jenkins@devops-2026.local"

                                    git add feedback.txt

                                    if git diff --cached --quiet; then
                                        echo "No feedback changes to commit."
                                    else
                                        git commit -m "[JENKINS-FEEDBACK] Update test feedback"
                                        git push origin HEAD:main
                                    fi
                                '''
                            } else {
                                bat '''
                                    git config user.name "Jenkins"
                                    git config user.email "jenkins@devops-2026.local"

                                    git add feedback.txt

                                    git diff --cached --quiet
                                    if %ERRORLEVEL% EQU 0 (
                                        echo No feedback changes to commit.
                                    ) else (
                                        git commit -m "[JENKINS-FEEDBACK] Update test feedback"
                                        git push origin HEAD:main
                                    )
                                '''
                            }
                        }
                    } catch (Exception e) {
                        echo "Warning: Push feedback step failed (${e.message}). Ensure Jenkins has valid Git credentials configured."
                    }
                }
            }
        }
    }

    post {
        always {
            junit(
                testResults: '**/*test-results.xml',
                allowEmptyResults: true
            )

            archiveArtifacts(
                artifacts: 'feedback.txt, **/*test-results.xml, frontend/dist/**',
                fingerprint: true,
                allowEmptyArchive: true
            )

            echo "Build completed with status: ${currentBuild.currentResult}"
        }

        success {
            echo 'Jenkins pipeline completed successfully.'
        }

        failure {
            echo 'Jenkins pipeline failed.'
        }

        unstable {
            echo 'Tests failed, but feedback was generated successfully.'
        }
    }
}

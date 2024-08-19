pipeline {
    agent {
        docker { image 'mcr.microsoft.com/playwright/python:v1.38.0-jammy' }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            parallel {
                 stage('Chromium Tests') {
                    steps {
                        script {
                            // Execute Playwright tests for Chromium
                             sh 'python -m pytest -m ui --browser chromium --cucumberjson=cucumber_report_chrome.json'
                             cucumber buildStatus: 'UNSTABLE',
                                reportTitle: 'Chromium report',
                                fileIncludePattern: 'cucumber_report_chrome.json',
                                trendsLimit: 10,
                                classifications: [
                                    [
                                        'key': 'Browser',
                                        'value': 'Chrome'
                                    ]
                                ]
                             sh 'rm -f cucumber_report_chrome.json'
                        }
                    }
                }
                stage('Firefox Tests') {
                    steps {
                        script {
                            // Execute Playwright tests for Firefox
                             sh 'python -m pytest -m ui --browser firefox --cucumberjson=cucumber_report_firefox.json'
                             cucumber buildStatus: 'UNSTABLE',
                                reportTitle: 'Firefox report',
                                fileIncludePattern: 'cucumber_report_firefox.json',
                                trendsLimit: 10,
                                classifications: [
                                    [
                                        'key': 'Browser',
                                        'value': 'Firefox'
                                    ]
                                ]
                             sh 'rm -f cucumber_report_firefox.json'
                        }
                    }
                }
                stage('Api Tests') {
                    steps {
                        script {
                            // Execute Playwright API tests
                             sh 'python -m pytest -m api --browser chromium --cucumberjson=cucumber_report_api.json'
                             cucumber buildStatus: 'UNSTABLE',
                                reportTitle: 'Api report',
                                fileIncludePattern: 'cucumber_report_api.json',
                                trendsLimit: 10
                             sh 'rm -f cucumber_report_api.json'
                        }
                    }
                }
            }

        }
    }
}
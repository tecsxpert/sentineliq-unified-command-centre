@echo off
REM Describe Endpoint - cURL Test Suite (Day 3)
REM Run from: ai-service directory
REM Usage: describe_api_tests.bat
REM Make sure Flask app is running (python app.py)

echo.
echo ================================================================================
echo     DESCRIBE ENDPOINT - API TESTING
echo ================================================================================
echo.
echo Prerequisites:
echo  - Flask app running: python app.py
echo  - curl installed on Windows
echo  - .env file with GROQ_API_KEY configured
echo.
echo ================================================================================

REM Test 1: Health check
echo.
echo [TEST 1] Health Check
echo ================================================================================
echo GET http://localhost:5000/api/ai/health
echo.
curl -s http://localhost:5000/api/ai/health | python -m json.tool
echo.

REM Test 2: Describe - Bug Report
echo.
echo [TEST 2] Describe - Login Bug
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
echo REQUEST:
set input1=When I try to login with my email and password, it keeps saying 'Invalid credentials' even though I'm 100%% sure my credentials are correct. This happened after the latest update. Also, the error message doesn't help at all. I've tried resetting my password but still getting the same error. Works fine on mobile app though.
echo {
echo   "text": "%input1%"
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input1%\"}" | python -m json.tool
echo.

REM Test 3: Describe - Feature Request
echo.
echo [TEST 3] Describe - Dark Mode Feature Request
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
set input2=It would be amazing if we could have a dark mode option. Eye strain during late night usage is real. Maybe add a toggle in settings that switches between light and dark themes automatically based on system preference?
echo REQUEST:
echo {
echo   "text": "%input2%"
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input2%\"}" | python -m json.tool
echo.

REM Test 4: Describe - Performance Issue
echo.
echo [TEST 4] Describe - Performance Issue
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
set input3=The dashboard loads super slow. On my 5G connection it takes like 10 seconds just to see the initial content. I'm running Chrome on MacBook. The network tab shows tons of API calls happening. Can you optimize the data loading or implement caching?
echo REQUEST:
echo {
echo   "text": "%input3%"
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input3%\"}" | python -m json.tool
echo.

REM Test 5: Describe - Feature Request Export
echo.
echo [TEST 5] Describe - Export Feature
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
set input4=Currently, there's no way to export my data. I need to be able to download reports as CSV or PDF format. This would help with my analysis workflow and help me share data with team members who don't have access to the app.
echo REQUEST:
echo {
echo   "text": "%input4%"
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input4%\"}" | python -m json.tool
echo.

REM Test 6: Describe - UI Feedback
echo.
echo [TEST 6] Describe - UI Button Feedback
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
set input5=The button colors could be better. The primary action button doesn't stand out enough from the secondary buttons. I had to click around for 30 seconds to figure out which button to press for the main action. Maybe use a more vibrant color?
echo REQUEST:
echo {
echo   "text": "%input5%"
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input5%\"}" | python -m json.tool
echo.

REM Test 7: Error - Empty text
echo.
echo [TEST 7] Error Handling - Empty Text
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
echo REQUEST:
echo {
echo   "text": ""
echo }
echo.
echo RESPONSE (should be 400):
curl -s -w "\nStatus: %%{http_code}\n" -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"\"}" | python -m json.tool
echo.

REM Test 8: Error - Missing text field
echo.
echo [TEST 8] Error Handling - Missing 'text' Field
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
echo REQUEST:
echo {
echo   "other_field": "value"
echo }
echo.
echo RESPONSE (should be 400):
curl -s -w "\nStatus: %%{http_code}\n" -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"other_field\": \"value\"}" | python -m json.tool
echo.

REM Test 9: With cache disabled
echo.
echo [TEST 9] Describe - Cache Disabled
echo ================================================================================
echo POST http://localhost:5000/api/ai/describe
echo.
set input6=Fix the login bug please
echo REQUEST:
echo {
echo   "text": "%input6%",
echo   "use_cache": false
echo }
echo.
echo RESPONSE:
curl -s -X POST http://localhost:5000/api/ai/describe ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"%input6%\", \"use_cache\": false}" | python -m json.tool
echo.

echo.
echo ================================================================================
echo TEST SUITE COMPLETE
echo ================================================================================
echo.
pause

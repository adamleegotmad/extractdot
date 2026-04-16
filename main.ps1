Write-Host "Step 1: convert.py" -ForegroundColor Cyan
python convert.py

Write-Host "Step 2: regular.py" -ForegroundColor Cyan
python regular.py

Write-Host "Step 3: choose.py" -ForegroundColor Cyan
python choose.py   # 此处会等待您的输入

Write-Host "Step 4: final.py" -ForegroundColor Cyan
python final.py
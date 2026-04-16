#!/bin/bash
# 不使用 set -e，改为手动检查每一步的返回值

run_step() {
    echo ">>> $1"
    shift
    "$@"
    if [ $? -ne 0 ]; then
        echo "❌ 命令执行失败: $*"
        exit 1
    fi
    echo "✅ 完成"
}

run_step "Step 1: Converting to binary images..." python3 convert.py
run_step "Step 2: Normalizing coordinates..." python3 regular.py
run_step "Step 3: Selecting required points..." python3 choose.py
run_step "Step 4: Generating final extracted point coordinates..." python3 final.py

echo "🎉 All steps completed successfully."
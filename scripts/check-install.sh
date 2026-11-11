#!/usr/bin/env bash
set -euo pipefail
APK=${1:-app/build/outputs/apk/debug/app-debug.apk}
PACKAGE=${2:-pl.neonempire.game.debug}
adb install -r "$APK"
adb shell pm path "$PACKAGE" | grep 'package:'
adb logcat -c
adb shell am start -W -n "$PACKAGE/pl.neonempire.game.MainActivity" | tee /tmp/neon-launch.txt
grep -q 'Status: ok' /tmp/neon-launch.txt
sleep 10
adb shell pidof "$PACKAGE"
adb logcat -d > /tmp/neon-logcat.txt
if grep -E 'FATAL EXCEPTION|Uncaught (SyntaxError|ReferenceError|TypeError)' /tmp/neon-logcat.txt; then exit 1; fi

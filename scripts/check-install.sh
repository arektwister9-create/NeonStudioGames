#!/usr/bin/env bash
set -euo pipefail
APK=app/build/outputs/apk/debug/app-debug.apk
adb install -r "$APK"
adb shell pm path pl.neonempire.game.debug | grep 'package:'
adb logcat -c
adb shell am start -W -n pl.neonempire.game.debug/pl.neonempire.game.MainActivity | tee /tmp/neon-launch.txt
grep -q 'Status: ok' /tmp/neon-launch.txt
sleep 10
adb shell pidof pl.neonempire.game.debug
adb logcat -d > /tmp/neon-logcat.txt
if grep -E 'FATAL EXCEPTION|Uncaught (SyntaxError|ReferenceError|TypeError)' /tmp/neon-logcat.txt; then exit 1; fi

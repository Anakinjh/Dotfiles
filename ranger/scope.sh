#!/usr/bin/env bash

set -e
set -x  # Enable debugging

FILE_PATH="$1"
PV_WIDTH="${2:-80}"
PV_HEIGHT="${3:-40}"
IMAGE_CACHE_PATH="$4"
PV_IMAGE_ENABLED="${5:-True}"

handle_image() {
    case "$1" in
        image/*)
            ueberzug layer --parser bash --silent <<EOF
            {
                "action": "add",
                "identifier": "preview",
                "x": 0,
                "y": 0,
                "width": "${PV_WIDTH}",
                "height": "${PV_HEIGHT}",
                "path": "${FILE_PATH}",
                "scaler": "fit_contain"
            }
EOF
            exit 0
            ;;
    esac
}

MIMETYPE=$(file --mime-type -b "$FILE_PATH")

if [ "$PV_IMAGE_ENABLED" = "True" ]; then
    handle_image "$MIMETYPE"
fi

case "$MIMETYPE" in
    text/* | */xml | application/json)
        if command -v highlight >/dev/null 2>&1; then
            highlight --out-format=ansi "$FILE_PATH" && exit 0
        elif command -v pygmentize >/dev/null 2>&1; then
            pygmentize -g "$FILE_PATH" && exit 0
        else
            cat "$FILE_PATH" && exit 0
        fi;;
    application/pdf)
        if command -v pdftotext >/dev/null 2>&1; then
            pdftotext -l 10 -nopgbrk -q "$FILE_PATH" - && exit 0
        fi;;
    *)
        file "$FILE_PATH" && exit 0;;
esac

exit 1


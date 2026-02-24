#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 4 ]; then
	echo "Usage: $0 <signed_url> <width> <height> <output_path>"
	exit 1
fi

signed_url="$1"
width="$2"
height="$3"
output_path="$4"

if ! [[ "$width" =~ ^[0-9]+$ && "$height" =~ ^[0-9]+$ ]]; then
	echo "Error: width and height must be integers."
	exit 1
fi

mkdir -p "$(dirname "$output_path")"

normalized_url="$signed_url"
if [[ "$signed_url" == *"googleusercontent.com"* ]]; then
	# googleusercontent images frequently default to a small preview unless a size
	# suffix is provided. Strip any existing "=w...-h..." suffix (and flags) and
	# append the requested dimensions.
	base_url="$(printf '%s' "$signed_url" | sed -E 's/=w[0-9]+-h[0-9]+.*$//')"
	normalized_url="${base_url}=w${width}-h${height}"
fi

echo "Downloading screenshot..."
curl -fL --retry 3 --retry-delay 1 --connect-timeout 10 --compressed \
	"$normalized_url" \
	-o "$output_path"

actual_width=""
actual_height=""
if command -v sips >/dev/null 2>&1; then
	actual_width="$(sips -g pixelWidth "$output_path" | awk '/pixelWidth:/{print $2}')"
	actual_height="$(sips -g pixelHeight "$output_path" | awk '/pixelHeight:/{print $2}')"
	echo "Downloaded image size: ${actual_width}x${actual_height}"
	if [ "$actual_width" != "$width" ] || [ "$actual_height" != "$height" ]; then
		echo "Error: expected ${width}x${height} but got ${actual_width}x${actual_height}."
		exit 1
	fi
else
	echo "Warning: sips not found; skipped local resolution verification."
fi

url_sha256_12="$(printf '%s' "$signed_url" | shasum -a 256 | awk '{print $1}' | cut -c1-12)"
file_sha256_12="$(shasum -a 256 "$output_path" | awk '{print $1}' | cut -c1-12)"

echo "Saved to: $output_path"
echo "download_url_sha256_12: $url_sha256_12"
echo "sha256_12: $file_sha256_12"
echo "Reminder: do not commit signed URLs."


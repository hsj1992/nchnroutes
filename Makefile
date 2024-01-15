# Makefile

.PHONY: all

all: check

# Download the latest SHA256 files
delegated-apnic-latest.sha256:
	curl -o delegated-apnic-latest.sha256 https://raw.githubusercontent.com/hsj1992/nchnroutes/main/delegated-apnic-latest.sha256

china_ip_list.txt.sha256:
	curl -o china_ip_list.txt.sha256 https://raw.githubusercontent.com/hsj1992/nchnroutes/main/china_ip_list.txt.sha256

# Check if local files match the downloaded SHA256 files
check: delegated-apnic-latest.sha256 china_ip_list.txt.sha256
	@sha256sum -c $^ || \
		(echo "Files do not match. Continue Running ..." && \
		git pull && \
		python3 fordomain.py && \
		mv routes4.conf /etc/bird/routes4.conf && \
		birdc configure)


.PHONY: fmt
fmt:
	python -m pip install -q black >/dev/null 2>&1 || true
	black dayledger tests

INSTALL_PREFIX:=/etc/systemd/system

SERVICES:=$(shell ls *.service)
TARGETS:=$(addprefix ${INSTALL_PREFIX}/, ${SERVICES})
all: ${TARGETS}

echo:
	echo "${TARGETS}"

${INSTALL_PREFIX}/%.service: %.service
	chmod a+rx $^
	cp $^ $@
	systemctl enable $^


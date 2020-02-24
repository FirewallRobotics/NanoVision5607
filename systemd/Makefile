INSTALL_PREFIX:=/etc/systemd/system

TARGETS:=$(shell ls *.service)
TARGETS:=$(addprefix ${INSTALL_PREFIX}/, ${TARGETS})
all: ${TARGETS}

echo:
	echo "${TARGETS}"

${INSTALL_PREFIX}/%.service: %.service
	chmod a+rx $^
	cp $^ $@

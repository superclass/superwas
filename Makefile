# AIX/Linux install
INSTALL=/usr/bin/install
# Target directory
BINDIR=/opt/scripts/superwas
LIBDIR=${BINDIR}/lib

SCRIPTS=server.properties \
build.properties \
log4j.properties \
Util.py \
application.py \
cell.py \
cluster.py \
config.py \
datasource.py \
dynamicsslconfigselection.py \
jaas.py \
jms.py \
mail.py \
nagios.py \
namespacebinding.py \
node.py \
objectcache.py \
replication.py \
scheduler.py \
server.py \
sharedlibrary.py \
sslconfig.py \
superwas.py \
url.py \
virtualhost.py \
wasconfig.py \
wasvariable.py \
workmanager.py

EXE=superwas

USER=superwas
GROUP=was

LOG4J=lib/log4j-1.2.8.jar

all: install

clean:
	@rm -rf $(BINDIR)

install-dir:
# Create directory if it does not exist
	@if [ -d $(BINDIR) ]; then \
    echo "Directory $(BINDIR) already exists, remove it and rerun the install."\
  else \
    mkdir -m 755 -p $(BINDIR); mkdir -m 755 -p $(BINDIR)/lib; \
  fi

install-bin: $(SCRIPTS)
	$(INSTALL) -o $(USER) -g $(GROUP) -m 644 $? $(BINDIR)

install-exe: $(EXE)
	$(INSTALL) -o $(USER) -g $(GROUP) -m 755 $? $(BINDIR)

install-lib:
	$(INSTALL) -o $(USER) -g $(GROUP) -m 644 $(LOG4J) $(LIBDIR)

install: install-dir install-bin install-lib install-exe

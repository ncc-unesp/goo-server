# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
BUILDDIR      = ../portal/static/

.PHONY: clean html

clean:
	-rm -rf $(BUILDDIR)/*

html:
	$(SPHINXBUILD) -b html api/ $(BUILDDIR)/api/
	$(SPHINXBUILD) -b html user/ $(BUILDDIR)/user/
	$(SPHINXBUILD) -b html developer/ $(BUILDDIR)/developer/
	$(SPHINXBUILD) -b html architecture/ $(BUILDDIR)/architecture/
	$(SPHINXBUILD) -b html home/ $(BUILDDIR)/
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

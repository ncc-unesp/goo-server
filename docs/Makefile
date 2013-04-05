# Makefile for Sphinx documentation

# You can set these variables from the command line.
SPHINXBUILD   = sphinx-build
BUILDDIR      = ../portal/static/docs

.PHONY: clean html

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(BUILDDIR)/.buildinfo
	rm -rf $(BUILDDIR)/.doctrees

html:
	$(SPHINXBUILD) -b html api/ $(BUILDDIR)/api/
	$(SPHINXBUILD) -b html architecture/ $(BUILDDIR)/architecture/
	$(SPHINXBUILD) -b html developer/ $(BUILDDIR)/developer/
	$(SPHINXBUILD) -b html home/ $(BUILDDIR)/
	$(SPHINXBUILD) -b html user/ $(BUILDDIR)/user/
	@echo
	@echo "Build finished. The HTML pages are in $(BUILDDIR)"

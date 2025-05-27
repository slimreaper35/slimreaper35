#!/usr/bin/env python3

from PyPDF2 import PdfMerger

RESUME_FILE = "msoltis-resume.pdf"
WINGFINDER_FILE = "wingfinder.pdf"

OUTPUT_FILE = "msoltis-resume-plus.pdf"

reader = PdfMerger()
reader.append(RESUME_FILE)
reader.append(WINGFINDER_FILE)
reader.write(OUTPUT_FILE)
reader.close()

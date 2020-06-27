# Prepare Flat, Broken, Inlined Garbage

Say you've written a paper in LaTeX.

Some journals require the source to compile the published version.  Unfortunately, their software is insane; and can't handle many features anyone would take for granted.  For example, maybe macros are straight-up forbidden.  That's a problem if you have literally hundreds/thousands of macro usages.  You know, as you do.

Maybe they go further.  You have to have all your files in one directory.  And PGF plots can't load CSV data tables because their bronze-age submission software literally thinks anything so futuristic as a ".csv" must be an actual video.

Yes; it's a reputable journal.  No; they somehow don't care that it's a problem—that besides the gross human cost it extracts in mindless tedium from doctorate-level academicians, the frustration and complications are actually inimical to the very end goal of Science itself.  Yes; this is the only way they will accept it.  No, you can't regular-expression your way out of this mess because LaTeX is not a regular grammar.  You obviously can't do such a monumental task as break everything by hand (even if you were willing, which you are quite rightly *not*, you don't have the time anyway).

---

Basically, this project is a preprocessor for evaluating/inlining/applying LaTeX macros, that also supports several other transforms associated with restrictive, bad paper submission systems.  The whole thing will be dumped into a new temporary directory, which you can then just upload.  It was good enough to munge over my own paper, so I hope it is good enough to help you.  I hope that we, as a community, shall not waste any more time with this asinine publisher make-work nonsense, and get back to doing the research that *matters* that we all want to be doing *anyway*.



## Usage

Drop (a copy of, for safety; the input isn't changed, but maybe I made a mistake) your project into this directory.  The main LaTeX file should be in this directory.  Then, edit the user-configurable section in "[main.py](main.py)" to point to it, and make sure you understand what the program does.  Then just run python on "[main.py](main.py)".



## Contributions

Are welcome.  Highly valued are expansions of the functionality / workarounds for other ways that stupid submission systems fail to do their only job, that I didn't happen to encounter.



## Credits and License

A major portion of this code's functionality is due to the excellent [latex.py](https://github.com/jobh/latex.py) which, being a pre-requisite, is included here.  This resource is currently licensed under GPL 2 or newer, which is compatible with the rest of this project's (much less-restrictive) MIT license.
